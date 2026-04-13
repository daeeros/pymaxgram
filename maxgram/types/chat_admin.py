from __future__ import annotations

from .base import MaxObject


class ChatAdmin(MaxObject):
    """Admin assignment request."""

    user_id: int
    permissions: list[str] | None = None
    alias: str | None = None
