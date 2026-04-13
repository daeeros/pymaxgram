from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import Message


class GetPinnedMessage(MaxMethod[Message | None]):
    """GET /chats/{chat_id}/pin - Get pinned message."""

    __returning__: ClassVar[type] = Message
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/chats/{chat_id}/pin"

    chat_id: int
