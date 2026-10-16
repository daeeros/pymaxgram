from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types.new_message_link import NewMessageLink


class EditComment(MaxMethod[bool]):
    """PUT /messages/{message_id}/comments - Edit a comment.

    Only within 26 hours of posting (``comments.timeout_exceeded`` otherwise).
    Without the ``edit`` admin right the bot can edit only its own comments.
    """

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "PUT"
    __api_path__: ClassVar[str] = "/messages/{message_id}/comments"

    message_id: str
    comment_id: str
    text: str | None = None
    link: NewMessageLink | None = None
    format: str | None = None

    def build_query_params(self) -> dict[str, Any]:
        return {"comment_id": self.comment_id}

    def build_request_body(self) -> dict[str, Any] | None:
        body: dict[str, Any] = {}
        if self.text is not None:
            body["text"] = self.text
        if self.link is not None:
            body["link"] = self.link.model_dump(exclude_none=True)
        if self.format is not None:
            body["format"] = self.format
        return body if body else None
