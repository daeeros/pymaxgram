from __future__ import annotations

from typing import Any

from .base import MutableMaxObject
from .update import Update


class ErrorEvent(MutableMaxObject):
    """Error event wrapper for error handlers."""

    update: Update
    exception: Exception
