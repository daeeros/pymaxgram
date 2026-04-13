from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import Subscription


class GetSubscriptions(MaxMethod[list[Subscription]]):
    """GET /subscriptions - List webhook subscriptions."""

    __returning__: ClassVar[type] = list
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/subscriptions"
