from __future__ import annotations

from typing import Any

from maxgram.enums.chat_type import ChatType
from maxgram.filters.base import Filter
from maxgram.types import MaxObject

ChatTypeType = str | ChatType


def resolve_chat_type(event: Any) -> str | None:
    """Extract the chat type from any event that carries a recipient.

    Works for :class:`~maxgram.types.Message`, :class:`~maxgram.types.Callback`
    (via its attached message) and :class:`~maxgram.types.Update`.
    """
    recipient = getattr(event, "recipient", None)
    if recipient is None:
        message = getattr(event, "message", None)
        recipient = getattr(message, "recipient", None)
    return getattr(recipient, "chat_type", None)


class ChatTypeFilter(Filter):
    """Pass only events coming from chats of the given type(s).

    .. code-block:: python

        @router.message(ChatTypeFilter(ChatType.CHANNEL))
        async def on_channel_post(message: Message): ...
    """

    __slots__ = ("chat_types",)

    def __init__(self, *chat_types: ChatTypeType) -> None:
        if not chat_types:
            msg = "At least one chat type is required"
            raise ValueError(msg)

        self.chat_types = tuple(
            chat_type.value if isinstance(chat_type, ChatType) else chat_type
            for chat_type in chat_types
        )

    async def __call__(self, event: MaxObject, *args: Any, **kwargs: Any) -> bool:
        chat_type = resolve_chat_type(event)
        return chat_type is not None and chat_type in self.chat_types

    def __str__(self) -> str:
        return self._signature_to_string(*self.chat_types)


class ChannelPost(ChatTypeFilter):
    """Pass only posts published in a channel.

    Shorthand for ``ChatTypeFilter(ChatType.CHANNEL)``.

    .. code-block:: python

        @router.message(ChannelPost())
        async def on_channel_post(message: Message):
            await message.reply("comment from the bot")
    """

    def __init__(self) -> None:
        super().__init__(ChatType.CHANNEL)
