from __future__ import annotations

from typing import Any

from .base import MaxObject


class Attachment(MaxObject):
    """Base attachment type."""

    type: str
    payload: Any | None = None


class PhotoAttachment(Attachment):
    """Photo/image attachment."""

    type: str = "image"


class VideoAttachment(Attachment):
    """Video attachment."""

    type: str = "video"


class AudioAttachment(Attachment):
    """Audio attachment."""

    type: str = "audio"


class FileAttachment(Attachment):
    """File attachment."""

    type: str = "file"


class StickerAttachment(Attachment):
    """Sticker attachment."""

    type: str = "sticker"


class ContactAttachment(Attachment):
    """Contact attachment."""

    type: str = "contact"


class InlineKeyboardAttachment(Attachment):
    """Inline keyboard attachment."""

    type: str = "inline_keyboard"


class LocationAttachment(Attachment):
    """Location attachment."""

    type: str = "location"


class ShareAttachment(Attachment):
    """Share attachment."""

    type: str = "share"
