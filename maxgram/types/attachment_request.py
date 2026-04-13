from __future__ import annotations

from typing import Any

from .base import MaxObject
from .button import Button


class AttachmentRequest(MaxObject):
    """Base attachment request for sending messages."""

    type: str
    payload: Any | None = None


class PhotoAttachmentRequest(AttachmentRequest):
    """Photo attachment request."""

    type: str = "image"


class VideoAttachmentRequest(AttachmentRequest):
    """Video attachment request."""

    type: str = "video"


class AudioAttachmentRequest(AttachmentRequest):
    """Audio attachment request."""

    type: str = "audio"


class FileAttachmentRequest(AttachmentRequest):
    """File attachment request."""

    type: str = "file"


class InlineKeyboardAttachmentRequest(AttachmentRequest):
    """Inline keyboard attachment request."""

    type: str = "inline_keyboard"
    payload: dict[str, list[list[dict[str, Any]]]] | None = None

    @classmethod
    def from_buttons(cls, buttons: list[list[Button]]) -> InlineKeyboardAttachmentRequest:
        """Create inline keyboard attachment from button rows."""
        return cls(
            payload={
                "buttons": [
                    [btn.model_dump(exclude_none=True) for btn in row]
                    for row in buttons
                ]
            }
        )
