from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import CommentMessage
from maxgram.types.new_message_link import NewMessageLink


class SendComment(MaxMethod[CommentMessage]):
    """POST /messages/{message_id}/comments - Comment a channel post.

    Comments take no attachments. Bot must be a channel admin with
    ``read_all_messages`` and ``write``, and comments must be enabled.
    """

    __returning__: ClassVar[type] = CommentMessage
    __http_method__: ClassVar[str] = "POST"
    __api_path__: ClassVar[str] = "/messages/{message_id}/comments"

    message_id: str
    text: str | None = None
    link: NewMessageLink | None = None
    format: str | None = None
    disable_link_preview: bool | None = None

    def build_query_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if self.disable_link_preview is not None:
            params["disable_link_preview"] = str(self.disable_link_preview).lower()
        return params

    def build_request_body(self) -> dict[str, Any] | None:
        body: dict[str, Any] = {}
        if self.text is not None:
            body["text"] = self.text
        if self.link is not None:
            body["link"] = self.link.model_dump(exclude_none=True)
        if self.format is not None:
            body["format"] = self.format
        return body if body else None
