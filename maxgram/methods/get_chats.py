from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import Chat


class ChatList(MaxMethod):
    """Wrapper for chat list response."""
    pass


class GetChats(MaxMethod[list[Chat]]):
    """GET /chats - List all group chats."""

    __returning__: ClassVar[type] = list
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/chats"

    count: int | None = None
    marker: int | None = None
