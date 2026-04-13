from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod


class CreateSubscription(MaxMethod[bool]):
    """POST /subscriptions - Subscribe to updates (webhook)."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "POST"
    __api_path__: ClassVar[str] = "/subscriptions"

    url: str
    update_types: list[str] | None = None
    secret: str | None = None
