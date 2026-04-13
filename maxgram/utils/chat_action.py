from __future__ import annotations

import asyncio
import logging
import time
from asyncio import Event, Lock
from contextlib import suppress
from types import TracebackType
from typing import Any

from maxgram import Bot

logger = logging.getLogger(__name__)
DEFAULT_INTERVAL = 5.0
DEFAULT_INITIAL_SLEEP = 0.0


class ChatActionSender:
    """
    Automatically send chat action until a long operation is done.

    MAX supported actions: typing_on, sending_photo, sending_video,
    sending_audio, sending_file, mark_seen
    """

    def __init__(
        self,
        *,
        bot: Bot,
        chat_id: int,
        action: str = "typing_on",
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> None:
        self.chat_id = chat_id
        self.action = action
        self.interval = interval
        self.initial_sleep = initial_sleep
        self.bot = bot

        self._lock = Lock()
        self._close_event = Event()
        self._closed_event = Event()
        self._task: asyncio.Task[Any] | None = None

    @property
    def running(self) -> bool:
        return bool(self._task)

    async def _wait(self, interval: float) -> None:
        with suppress(asyncio.TimeoutError):
            await asyncio.wait_for(self._close_event.wait(), interval)

    async def _worker(self) -> None:
        try:
            counter = 0
            await self._wait(self.initial_sleep)
            while not self._close_event.is_set():
                start = time.monotonic()
                await self.bot.send_action(
                    chat_id=self.chat_id,
                    action=self.action,
                )
                counter += 1
                interval = self.interval - (time.monotonic() - start)
                await self._wait(interval)
        finally:
            self._closed_event.set()

    async def _run(self) -> None:
        async with self._lock:
            self._close_event.clear()
            self._closed_event.clear()
            if self.running:
                msg = "Already running"
                raise RuntimeError(msg)
            self._task = asyncio.create_task(self._worker())

    async def _stop(self) -> None:
        async with self._lock:
            if not self.running:
                return
            if not self._close_event.is_set():
                self._close_event.set()
                await self._closed_event.wait()
            self._task = None

    async def __aenter__(self) -> ChatActionSender:
        await self._run()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> Any:
        await self._stop()

    @classmethod
    def typing(
        cls,
        chat_id: int,
        bot: Bot,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> ChatActionSender:
        return cls(bot=bot, chat_id=chat_id, action="typing_on",
                   interval=interval, initial_sleep=initial_sleep)

    @classmethod
    def sending_photo(
        cls,
        chat_id: int,
        bot: Bot,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> ChatActionSender:
        return cls(bot=bot, chat_id=chat_id, action="sending_photo",
                   interval=interval, initial_sleep=initial_sleep)

    @classmethod
    def sending_video(
        cls,
        chat_id: int,
        bot: Bot,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> ChatActionSender:
        return cls(bot=bot, chat_id=chat_id, action="sending_video",
                   interval=interval, initial_sleep=initial_sleep)

    @classmethod
    def sending_file(
        cls,
        chat_id: int,
        bot: Bot,
        interval: float = DEFAULT_INTERVAL,
        initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> ChatActionSender:
        return cls(bot=bot, chat_id=chat_id, action="sending_file",
                   interval=interval, initial_sleep=initial_sleep)


