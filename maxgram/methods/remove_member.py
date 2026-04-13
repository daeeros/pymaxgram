from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod


class RemoveMember(MaxMethod[bool]):
    """DELETE /chats/{chat_id}/members - Remove member from chat."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "DELETE"
    __api_path__: ClassVar[str] = "/chats/{chat_id}/members"

    chat_id: int
    user_id: int
    block: bool | None = None
