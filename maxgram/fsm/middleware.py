from collections.abc import Awaitable, Callable
from typing import Any, cast

from maxgram import Bot
from maxgram.dispatcher.middlewares.base import BaseMiddleware
from maxgram.dispatcher.middlewares.user_context import EVENT_CONTEXT_KEY, EventContext
from maxgram.fsm.context import FSMContext
from maxgram.fsm.storage.base import (
    DEFAULT_DESTINY,
    BaseEventIsolation,
    BaseStorage,
    StorageKey,
)
from maxgram.fsm.strategy import FSMStrategy, apply_strategy
from maxgram.types import MaxObject


class FSMContextMiddleware(BaseMiddleware):
    def __init__(
        self,
        storage: BaseStorage,
        events_isolation: BaseEventIsolation,
        strategy: FSMStrategy = FSMStrategy.USER_IN_CHAT,
    ) -> None:
        self.storage = storage
        self.strategy = strategy
        self.events_isolation = events_isolation

    async def __call__(
        self,
        handler: Callable[[MaxObject, dict[str, Any]], Awaitable[Any]],
        event: MaxObject,
        data: dict[str, Any],
    ) -> Any:
        bot: Bot = cast(Bot, data["bot"])
        context = self.resolve_event_context(bot, data)
        data["fsm_storage"] = self.storage
        if context:
            async with self.events_isolation.lock(key=context.key):
                data.update({"state": context, "raw_state": await context.get_state()})
                return await handler(event, data)
        return await handler(event, data)

    def resolve_event_context(
        self,
        bot: Bot,
        data: dict[str, Any],
        destiny: str = DEFAULT_DESTINY,
    ) -> FSMContext | None:
        event_context: EventContext = cast(EventContext, data.get(EVENT_CONTEXT_KEY))
        return self.resolve_context(
            bot=bot,
            chat_id=event_context.chat_id,
            user_id=event_context.user_id,
            destiny=destiny,
        )

    def resolve_context(
        self,
        bot: Bot,
        chat_id: int | None,
        user_id: int | None,
        destiny: str = DEFAULT_DESTINY,
    ) -> FSMContext | None:
        if chat_id is None:
            chat_id = user_id
        elif user_id is None and self.strategy in {FSMStrategy.CHAT, FSMStrategy.CHAT_TOPIC}:
            user_id = chat_id

        if chat_id is not None and user_id is not None:
            chat_id, user_id, thread_id = apply_strategy(
                chat_id=chat_id,
                user_id=user_id,
                thread_id=None,
                strategy=self.strategy,
            )
            return self.get_context(
                bot=bot,
                chat_id=chat_id,
                user_id=user_id,
                destiny=destiny,
            )
        return None

    def get_context(
        self,
        bot: Bot,
        chat_id: int,
        user_id: int,
        destiny: str = DEFAULT_DESTINY,
    ) -> FSMContext:
        return FSMContext(
            storage=self.storage,
            key=StorageKey(
                user_id=user_id,
                chat_id=chat_id,
                bot_id=bot.id,
                destiny=destiny,
            ),
        )

    async def close(self) -> None:
        await self.storage.close()
        await self.events_isolation.close()
