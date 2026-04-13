from __future__ import annotations

from .base import MaxObject


class Recipient(MaxObject):
    """Message recipient - can be a chat or a user."""

    chat_id: int | None = None
    chat_type: str | None = None
    user_id: int | None = None
