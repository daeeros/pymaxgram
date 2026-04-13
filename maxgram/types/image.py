from __future__ import annotations

from .base import MaxObject


class Image(MaxObject):
    """Image object."""

    url: str
    token: str | None = None
    width: int | None = None
    height: int | None = None
