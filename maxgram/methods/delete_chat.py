from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod


class DeleteChat(MaxMethod[bool]):
    """DELETE /chats/{chat_id} - Delete group chat."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "DELETE"
    __api_path__: ClassVar[str] = "/chats/{chat_id}"

    chat_id: int
