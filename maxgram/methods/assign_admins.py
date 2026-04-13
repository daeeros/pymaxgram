from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod


class AssignAdmins(MaxMethod[bool]):
    """POST /chats/{chat_id}/members/admins - Assign admins."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "POST"
    __api_path__: ClassVar[str] = "/chats/{chat_id}/members/admins"

    chat_id: int
    admins: list[dict[str, Any]]
