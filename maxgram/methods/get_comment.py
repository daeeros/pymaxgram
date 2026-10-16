from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import CommentMessage


class GetComment(MaxMethod[CommentMessage]):
    """GET /messages/{message_id}/comments/{comment_id} - Get single comment."""

    __returning__: ClassVar[type] = CommentMessage
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/messages/{message_id}/comments/{comment_id}"

    message_id: str
    comment_id: str
