from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import Message


class GetMessages(MaxMethod[list[Message]]):
    """GET /messages - Get messages from chat or by IDs."""

    __returning__: ClassVar[type] = list
    __item_type__: ClassVar[type] = Message
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/messages"

    chat_id: int | None = None
    message_ids: list[str] | None = None
    count: int | None = None
