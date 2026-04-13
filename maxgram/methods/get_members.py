from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import ChatMember


class GetMembers(MaxMethod[list[ChatMember]]):
    """GET /chats/{chat_id}/members - Get chat members."""

    __returning__: ClassVar[type] = list
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/chats/{chat_id}/members"

    chat_id: int
    user_ids: list[int] | None = None
    marker: int | None = None
    count: int | None = None
