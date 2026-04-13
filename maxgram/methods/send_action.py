from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod


class SendAction(MaxMethod[bool]):
    """POST /chats/{chat_id}/actions - Send bot action to chat."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "POST"
    __api_path__: ClassVar[str] = "/chats/{chat_id}/actions"

    chat_id: int
    action: str  # typing_on, sending_photo, sending_video, sending_audio, sending_file, mark_seen
