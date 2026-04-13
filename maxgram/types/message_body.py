from __future__ import annotations

from .attachment import Attachment
from .base import MaxObject
from .markup import MarkupElement


class MessageBody(MaxObject):
    """Message body containing text and attachments."""

    mid: str
    seq: int = 0
    text: str | None = None
    attachments: list[Attachment] | None = None
    markup: list[MarkupElement] | None = None
