from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import Chat


class EditChat(MaxMethod[Chat]):
    """PATCH /chats/{chat_id} - Modify chat information."""

    __returning__: ClassVar[type] = Chat
    __http_method__: ClassVar[str] = "PATCH"
    __api_path__: ClassVar[str] = "/chats/{chat_id}"

    chat_id: int
    icon: dict[str, Any] | None = None
    title: str | None = None
    pin: str | None = None
    notify: bool | None = None
