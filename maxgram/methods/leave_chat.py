from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod


class LeaveChat(MaxMethod[bool]):
    """DELETE /chats/{chat_id}/members/me - Remove bot from chat."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "DELETE"
    __api_path__: ClassVar[str] = "/chats/{chat_id}/members/me"

    chat_id: int
