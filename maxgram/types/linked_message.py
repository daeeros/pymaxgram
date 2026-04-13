from __future__ import annotations

from typing import TYPE_CHECKING

from .base import MaxObject

if TYPE_CHECKING:
    from .message_body import MessageBody
    from .user import User


class LinkedMessage(MaxObject):
    """Linked message (forwarded or reply)."""

    type: str  # "forward" or "reply"
    sender: User | None = None
    chat_id: int | None = None
    message: MessageBody | None = None
