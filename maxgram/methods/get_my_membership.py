from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import ChatMember


class GetMyMembership(MaxMethod[ChatMember]):
    """GET /chats/{chat_id}/members/me - Get bot's membership info."""

    __returning__: ClassVar[type] = ChatMember
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/chats/{chat_id}/members/me"

    chat_id: int
