from __future__ import annotations

from .user import User


class UserWithPhoto(User):
    """User with avatar information."""

    avatar_url: str | None = None
    full_avatar_url: str | None = None
    description: str | None = None
