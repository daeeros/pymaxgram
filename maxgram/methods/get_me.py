from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import BotInfo


class GetMe(MaxMethod[BotInfo]):
    """GET /me - Get bot information."""

    __returning__: ClassVar[type] = BotInfo
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/me"
