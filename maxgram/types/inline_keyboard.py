from __future__ import annotations

from .base import MaxObject
from .button import Button


class InlineKeyboard(MaxObject):
    """Inline keyboard with rows of buttons."""

    buttons: list[list[Button]]
