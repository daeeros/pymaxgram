from __future__ import annotations

from .base import MaxObject


class Subscription(MaxObject):
    """Webhook subscription."""

    url: str
    time: int = 0
    update_types: list[str] | None = None
    version: str | None = None
