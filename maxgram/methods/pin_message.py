from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod


class PinMessage(MaxMethod[bool]):
    """PUT /chats/{chat_id}/pin - Pin message."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "PUT"
    __api_path__: ClassVar[str] = "/chats/{chat_id}/pin"

    chat_id: int
    message_id: str
    notify: bool | None = None
