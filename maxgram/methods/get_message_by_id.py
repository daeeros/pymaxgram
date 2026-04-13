from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import Message


class GetMessageById(MaxMethod[Message]):
    """GET /messages/{message_id} - Get single message."""

    __returning__: ClassVar[type] = Message
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/messages/{message_id}"

    message_id: str
