from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import CommentMessage


class GetComments(MaxMethod[list[CommentMessage]]):
    """GET /messages/{message_id}/comments - Get comments under a channel post.

    Newest comments come first. When ``comment_ids`` is set, only those
    comments are returned and the time filters are ignored.
    """

    __returning__: ClassVar[type] = list
    __item_type__: ClassVar[type] = CommentMessage
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/messages/{message_id}/comments"

    message_id: str
    comment_ids: list[str] | None = None
    before: int | None = None
    after: int | None = None
    count: int | None = None

    def build_query_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if self.comment_ids is not None:
            params["comment_ids"] = ",".join(self.comment_ids)
        if self.before is not None:
            params["before"] = self.before
        if self.after is not None:
            params["after"] = self.after
        if self.count is not None:
            params["count"] = self.count
        return params
