from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import Update


class GetUpdates(MaxMethod[list[Update]]):
    """GET /updates - Get updates via long polling."""

    __returning__: ClassVar[type] = list
    __item_type__: ClassVar[type] = Update
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/updates"

    limit: int | None = None
    timeout: int | None = None
    marker: int | None = None
    types: list[str] | None = None
