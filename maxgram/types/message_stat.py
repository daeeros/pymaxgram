from __future__ import annotations

from .base import MaxObject


class MessageStat(MaxObject):
    """Message statistics (for channels)."""

    views: int | None = None
