from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod


class DeleteSubscription(MaxMethod[bool]):
    """DELETE /subscriptions - Unsubscribe from updates."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "DELETE"
    __api_path__: ClassVar[str] = "/subscriptions"

    url: str
