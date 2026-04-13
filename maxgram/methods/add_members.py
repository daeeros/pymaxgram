from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod


class AddMembers(MaxMethod[bool]):
    """POST /chats/{chat_id}/members - Add members to chat."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "POST"
    __api_path__: ClassVar[str] = "/chats/{chat_id}/members"

    chat_id: int
    user_ids: list[int]
