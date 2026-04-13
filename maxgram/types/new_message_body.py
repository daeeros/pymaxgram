from __future__ import annotations

from .attachment_request import AttachmentRequest
from .base import MaxObject
from .new_message_link import NewMessageLink


class NewMessageBody(MaxObject):
    """Request body for creating/editing messages."""

    text: str | None = None
    attachments: list[AttachmentRequest] | None = None
    link: NewMessageLink | None = None
    notify: bool | None = None
    format: str | None = None  # "markdown" or "html"
