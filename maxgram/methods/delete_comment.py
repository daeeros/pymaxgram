from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod


class DeleteComment(MaxMethod[bool]):
    """DELETE /messages/{message_id}/comments - Delete a comment.

    Bot must be a channel admin with ``read_all_messages`` and ``delete``.
    """

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "DELETE"
    __api_path__: ClassVar[str] = "/messages/{message_id}/comments"

    message_id: str
    comment_id: str

    def build_query_params(self) -> dict[str, Any]:
        return {"comment_id": self.comment_id}
