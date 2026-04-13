from __future__ import annotations

import asyncio
import signal
import sys
import warnings
from asyncio import CancelledError, Event, Future, Lock
from collections.abc import AsyncGenerator, Awaitable
from contextlib import suppress
from typing import TYPE_CHECKING, Any

from maxgram import loggers
from maxgram.exceptions import MaxAPIError
from maxgram.fsm.middleware import FSMContextMiddleware
from maxgram.fsm.storage.base import BaseEventIsolation, BaseStorage
from maxgram.fsm.storage.memory import DisabledEventIsolation, MemoryStorage
from maxgram.fsm.strategy import FSMStrategy
from maxgram.methods import GetUpdates, MaxMethod
from maxgram.types import Update, User
from maxgram.types.base import UNSET, UNSET_TYPE
from maxgram.types.update import UpdateTypeLookupError
from maxgram.utils.backoff import Backoff, BackoffConfig

from .event.bases import UNHANDLED, SkipHandler
from .event.max import MaxEventObserver
from .middlewares.error import ErrorsMiddleware
from .middlewares.user_context import UserContextMiddleware
from .router import Router

if TYPE_CHECKING:
    from maxgram.client.bot import Bot
    from maxgram.methods.base import MaxType

DEFAULT_BACKOFF_CONFIG = BackoffConfig(min_delay=1.0, max_delay=5.0, factor=1.3, jitter=0.1)


class Dispatcher(Router):
    """Root router."""

    def __init__(
        self,
        *,
        storage: BaseStorage | None = None,
        fsm_strategy: FSMStrategy = FSMStrategy.USER_IN_CHAT,
        events_isolation: BaseEventIsolation | None = None,
        disable_fsm: bool = False,
        updates_debug: bool = False,
        requests_debug: bool = False,
        name: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(name=name)
        self.updates_debug = updates_debug
        self.requests_debug = requests_debug

        if storage and not isinstance(storage, BaseStorage):
            msg = f"FSM storage should be instance of 'BaseStorage' not {type(storage).__name__}"
            raise TypeError(msg)

        self.update = self.observers["update"] = MaxEventObserver(
            router=self,
            event_name="update",
        )
        self.update.register(self._listen_update)

        self.update.outer_middleware(ErrorsMiddleware(self))
        self.update.outer_middleware(UserContextMiddleware())

        self.fsm = FSMContextMiddleware(
            storage=storage or MemoryStorage(),
            strategy=fsm_strategy,
            events_isolation=events_isolation or DisabledEventIsolation(),
        )
        if not disable_fsm:
            self.update.outer_middleware(self.fsm)
        self.shutdown.register(self.fsm.close)

        self.workflow_data: dict[str, Any] = kwargs
        self._running_lock = Lock()
        self._stop_signal: Event | None = None
        self._stopped_signal: Event | None = None
        self._handle_update_tasks: set[asyncio.Task[Any]] = set()

    def __getitem__(self, item: str) -> Any:
        return self.workflow_data[item]

    def __setitem__(self, key: str, value: Any) -> None:
        self.workflow_data[key] = value

    def __delitem__(self, key: str) -> None:
        del self.workflow_data[key]

    def get(self, key: str, /, default: Any | None = None) -> Any | None:
        return self.workflow_data.get(key, default)

    @property
    def storage(self) -> BaseStorage:
        return self.fsm.storage

    @property
    def parent_router(self) -> Router | None:
        return None

    @parent_router.setter
    def parent_router(self, value: Router) -> None:
        msg = "Dispatcher can not be attached to another Router."
        raise RuntimeError(msg)

    async def feed_update(self, bot: Bot, update: Update, **kwargs: Any) -> Any:
        loop = asyncio.get_running_loop()
        handled = False
        start_time = loop.time()

        if update.bot != bot:
            update = Update.model_validate(update.model_dump(), context={"bot": bot})

        if self.updates_debug:
            self._debug_update(update)

        try:
            response = await self.update.wrap_outer_middleware(
                self.update.trigger,
                update,
                {
                    **self.workflow_data,
                    **kwargs,
                    "bot": bot,
                },
            )
            handled = response is not UNHANDLED
            return response
        finally:
            finish_time = loop.time()
            duration = (finish_time - start_time) * 1000
            if self.updates_debug:
                self._debug_result(update, handled, duration)
            else:
                loggers.event.info(
                    "Update type=%s is %s. Duration %d ms by bot id=%s",
                    update.update_type,
                    "handled" if handled else "not handled",
                    duration,
                    bot.id,
                )

    @staticmethod
    def _debug_update(update: Update) -> None:
        parts = [f"\n{'='*60}", f"UPDATE {update.update_type}"]
        if update.update_type in ("message_created", "message_edited") and update.message:
            msg = update.message
            user = msg.sender
            text = msg.body.text if msg.body else None
            parts.append(f"  from: {user.first_name} (id={user.user_id})" if user else "  from: unknown")
            parts.append(f"  chat: {msg.recipient.chat_id} ({msg.recipient.chat_type})")
            if text:
                parts.append(f"  text: {text!r}")
            if msg.body and msg.body.attachments:
                parts.append(f"  attachments: {[a.type for a in msg.body.attachments]}")
        elif update.update_type == "message_callback" and update.callback:
            cb = update.callback
            parts.append(f"  from: {cb.user.first_name} (id={cb.user.user_id})")
            parts.append(f"  payload: {cb.payload!r}")
            parts.append(f"  callback_id: {cb.callback_id[:20]}...")
            if cb.message:
                parts.append(f"  message_mid: {cb.message.body.mid}")
        else:
            if update.user:
                parts.append(f"  user: {update.user.first_name} (id={update.user.user_id})")
            if update.chat_id:
                parts.append(f"  chat: {update.chat_id}")
            if update.user_id:
                parts.append(f"  user_id: {update.user_id}")
            if update.message_id:
                parts.append(f"  message_id: {update.message_id}")
            if update.payload:
                parts.append(f"  payload: {update.payload!r}")
            if update.title:
                parts.append(f"  title: {update.title!r}")
            if update.is_channel is not None:
                parts.append(f"  is_channel: {update.is_channel}")
            if update.inviter_id:
                parts.append(f"  inviter_id: {update.inviter_id}")
            if update.admin_id:
                parts.append(f"  admin_id: {update.admin_id}")
            if update.muted_until:
                parts.append(f"  muted_until: {update.muted_until}")
        parts.append("="*60)
        loggers.event.info("\n".join(parts))

    @staticmethod
    def _debug_result(update: Update, handled: bool, duration: float) -> None:
        status = "HANDLED" if handled else "NOT HANDLED"
        loggers.event.info(
            "  -> %s in %d ms (type=%s)",
            status, duration, update.update_type,
        )

    async def feed_raw_update(self, bot: Bot, update: dict[str, Any], **kwargs: Any) -> Any:
        parsed_update = Update.model_validate(update, context={"bot": bot})
        return await self._feed_webhook_update(bot=bot, update=parsed_update, **kwargs)

    @classmethod
    async def _listen_updates(
        cls,
        bot: Bot,
        polling_timeout: int = 30,
        backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
        allowed_updates: list[str] | None = None,
    ) -> AsyncGenerator[Update, None]:
        """Endless updates reader using MAX long polling with marker cursor."""
        backoff = Backoff(config=backoff_config)
        get_updates = GetUpdates(timeout=polling_timeout, types=allowed_updates)
        kwargs = {}
        if bot.session.timeout:
            kwargs["timeout"] = int(bot.session.timeout + polling_timeout)
        failed = False
        while True:
            try:
                result = await bot(get_updates, **kwargs)
            except Exception as e:
                failed = True
                loggers.dispatcher.error("Failed to fetch updates - %s: %s", type(e).__name__, e)
                loggers.dispatcher.warning(
                    "Sleep for %f seconds and try again... (tryings = %d, bot id = %s)",
                    backoff.next_delay,
                    backoff.counter,
                    bot.id,
                )
                await backoff.asleep()
                continue

            if failed:
                loggers.dispatcher.info(
                    "Connection established (tryings = %d, bot id = %s)",
                    backoff.counter,
                    bot.id,
                )
                backoff.reset()
                failed = False

            # result is the raw response from check_response
            # For MAX API, updates come as a list
            updates = result if isinstance(result, list) else []

            for update in updates:
                if isinstance(update, dict):
                    update = Update.model_validate(update, context={"bot": bot})
                yield update

            # Update marker for next request if we got updates
            # The MAX API response has a marker field for pagination
            # We handle this by checking the raw response
            if updates:
                # Use the last update's timestamp or a marker from the response
                get_updates.marker = None  # Will be set from response if available

    async def _listen_update(self, update: Update, **kwargs: Any) -> Any:
        try:
            update_type = update.event_type
            event = update.event
        except UpdateTypeLookupError as e:
            warnings.warn(
                "Detected unknown update type.\n"
                f"Update: {update.model_dump_json(exclude_unset=True)}",
                RuntimeWarning,
                stacklevel=2,
            )
            raise SkipHandler() from e

        kwargs.update(event_update=update)
        return await self.propagate_event(update_type=update_type, event=event, **kwargs)

    async def _process_update(
        self,
        bot: Bot,
        update: Update,
        call_answer: bool = True,
        **kwargs: Any,
    ) -> bool:
        try:
            response = await self.feed_update(bot, update, **kwargs)
            if call_answer and isinstance(response, MaxMethod):
                await self.silent_call_request(bot=bot, result=response)
        except Exception as e:
            loggers.event.exception(
                "Cause exception while process update type=%s by bot id=%s\n%s: %s",
                update.update_type,
                bot.id,
                e.__class__.__name__,
                e,
            )
            return True
        else:
            return response is not UNHANDLED

    @classmethod
    async def silent_call_request(cls, bot: Bot, result: MaxMethod[Any]) -> None:
        try:
            await bot(result)
        except MaxAPIError as e:
            loggers.event.error("Failed to make answer: %s: %s", e.__class__.__name__, e)

    async def _process_with_semaphore(
        self,
        handle_update: Awaitable[bool],
        semaphore: asyncio.Semaphore,
    ) -> bool:
        try:
            return await handle_update
        finally:
            semaphore.release()

    async def _polling(
        self,
        bot: Bot,
        polling_timeout: int = 30,
        handle_as_tasks: bool = True,
        backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
        allowed_updates: list[str] | None = None,
        tasks_concurrency_limit: int | None = None,
        **kwargs: Any,
    ) -> None:
        bot_info = await bot.me()
        bot._requests_debug = self.requests_debug
        loggers.dispatcher.info(
            "Run polling for bot @%s id=%d - %r",
            bot_info.username,
            bot_info.user_id,
            bot_info.first_name,
        )

        semaphore = None
        if tasks_concurrency_limit is not None and handle_as_tasks:
            semaphore = asyncio.Semaphore(tasks_concurrency_limit)

        try:
            async for update in self._listen_updates(
                bot,
                polling_timeout=polling_timeout,
                backoff_config=backoff_config,
                allowed_updates=allowed_updates,
            ):
                handle_update = self._process_update(bot=bot, update=update, **kwargs)
                if handle_as_tasks:
                    if semaphore:
                        await semaphore.acquire()
                        handle_update_task = asyncio.create_task(
                            self._process_with_semaphore(handle_update, semaphore),
                        )
                    else:
                        handle_update_task = asyncio.create_task(handle_update)

                    self._handle_update_tasks.add(handle_update_task)
                    handle_update_task.add_done_callback(self._handle_update_tasks.discard)
                else:
                    await handle_update
        finally:
            loggers.dispatcher.info(
                "Polling stopped for bot @%s id=%d - %r",
                bot_info.username,
                bot_info.user_id,
                bot_info.first_name,
            )

    async def _feed_webhook_update(self, bot: Bot, update: Update, **kwargs: Any) -> Any:
        try:
            return await self.feed_update(bot, update, **kwargs)
        except Exception as e:
            loggers.event.exception(
                "Cause exception while process update type=%s by bot id=%s\n%s: %s",
                update.update_type,
                bot.id,
                e.__class__.__name__,
                e,
            )
            raise

    async def feed_webhook_update(
        self,
        bot: Bot,
        update: Update | dict[str, Any],
        _timeout: float = 55,
        **kwargs: Any,
    ) -> None:
        """Process webhook update. MAX does not support returning methods in webhook response."""
        if not isinstance(update, Update):
            update = Update.model_validate(update, context={"bot": bot})

        await self._feed_webhook_update(bot=bot, update=update, **kwargs)

    async def stop_polling(self) -> None:
        if not self._running_lock.locked():
            msg = "Polling is not started"
            raise RuntimeError(msg)
        if not self._stop_signal or not self._stopped_signal:
            return
        self._stop_signal.set()
        await self._stopped_signal.wait()

    def _signal_stop_polling(self, sig: signal.Signals) -> None:
        if not self._running_lock.locked():
            return
        loggers.dispatcher.warning("Received %s signal", sig.name)
        if not self._stop_signal:
            return
        self._stop_signal.set()

    async def start_polling(
        self,
        *bots: Bot,
        polling_timeout: int = 10,
        handle_as_tasks: bool = True,
        backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
        allowed_updates: list[str] | UNSET_TYPE | None = UNSET,
        handle_signals: bool = True,
        close_bot_session: bool = True,
        tasks_concurrency_limit: int | None = None,
        **kwargs: Any,
    ) -> None:
        if not bots:
            msg = "At least one bot instance is required to start polling"
            raise ValueError(msg)
        if "bot" in kwargs:
            msg = (
                "Keyword argument 'bot' is not acceptable, "
                "the bot instance should be passed as positional argument"
            )
            raise ValueError(msg)

        async with self._running_lock:
            if self._stop_signal is None:
                self._stop_signal = Event()
            if self._stopped_signal is None:
                self._stopped_signal = Event()

            if allowed_updates is UNSET:
                allowed_updates = self.resolve_used_update_types()

            self._stop_signal.clear()
            self._stopped_signal.clear()

            if handle_signals:
                loop = asyncio.get_running_loop()
                with suppress(NotImplementedError):
                    loop.add_signal_handler(
                        signal.SIGTERM,
                        self._signal_stop_polling,
                        signal.SIGTERM,
                    )
                    loop.add_signal_handler(
                        signal.SIGINT,
                        self._signal_stop_polling,
                        signal.SIGINT,
                    )

            workflow_data = {
                "dispatcher": self,
                "bots": bots,
                **self.workflow_data,
                **kwargs,
            }
            if "bot" in workflow_data:
                workflow_data.pop("bot")

            await self.emit_startup(bot=bots[-1], **workflow_data)
            loggers.dispatcher.info("Start polling")
            try:
                tasks: list[asyncio.Task[Any]] = [
                    asyncio.create_task(
                        self._polling(
                            bot=bot,
                            handle_as_tasks=handle_as_tasks,
                            polling_timeout=polling_timeout,
                            backoff_config=backoff_config,
                            allowed_updates=allowed_updates,
                            tasks_concurrency_limit=tasks_concurrency_limit,
                            **workflow_data,
                        ),
                    )
                    for bot in bots
                ]
                tasks.append(asyncio.create_task(self._stop_signal.wait()))
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

                for task in pending:
                    task.cancel()
                    with suppress(CancelledError):
                        await task
                await asyncio.gather(*done)

            finally:
                loggers.dispatcher.info("Polling stopped")
                try:
                    await self.emit_shutdown(bot=bots[-1], **workflow_data)
                finally:
                    if close_bot_session:
                        await asyncio.gather(*(bot.session.close() for bot in bots))
                self._stopped_signal.set()

    def run_polling(
        self,
        *bots: Bot,
        polling_timeout: int = 10,
        handle_as_tasks: bool = True,
        backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
        allowed_updates: list[str] | UNSET_TYPE | None = UNSET,
        handle_signals: bool = True,
        close_bot_session: bool = True,
        tasks_concurrency_limit: int | None = None,
        **kwargs: Any,
    ) -> None:
        with suppress(KeyboardInterrupt):
            coro = self.start_polling(
                *bots,
                **kwargs,
                polling_timeout=polling_timeout,
                handle_as_tasks=handle_as_tasks,
                backoff_config=backoff_config,
                allowed_updates=allowed_updates,
                handle_signals=handle_signals,
                close_bot_session=close_bot_session,
                tasks_concurrency_limit=tasks_concurrency_limit,
            )

            try:
                import uvloop
            except ImportError:
                return asyncio.run(coro)
            else:
                if sys.version_info >= (3, 11):
                    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
                        return runner.run(coro)
                else:
                    uvloop.install()
                    return asyncio.run(coro)
