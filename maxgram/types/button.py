from __future__ import annotations

from .base import MaxObject


class Button(MaxObject):
    """Inline keyboard button."""

    type: str
    text: str
    payload: str | None = None
    url: str | None = None
    intent: str | None = None
