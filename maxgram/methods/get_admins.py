from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import ChatMember


class GetAdmins(MaxMethod[list[ChatMember]]):
    """GET /chats/{chat_id}/members/admins - List admins."""

    __returning__: ClassVar[type] = list
    __item_type__: ClassVar[type] = ChatMember
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/chats/{chat_id}/members/admins"

    chat_id: int
    marker: int | None = None
