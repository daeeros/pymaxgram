from __future__ import annotations

from .base import MaxObject


class User(MaxObject):
    """MAX user object."""

    user_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    is_bot: bool = False
    last_activity_time: int | None = None
    name: str | None = None  # deprecated field
