from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import Message
from maxgram.types.new_message_link import NewMessageLink


class SendMessage(MaxMethod[Message]):
    """POST /messages - Send message to user or chat."""

    __returning__: ClassVar[type] = Message
    __http_method__: ClassVar[str] = "POST"
    __api_path__: ClassVar[str] = "/messages"

    chat_id: int | None = None
    user_id: int | None = None
    disable_link_preview: bool | None = None
    text: str | None = None
    attachments: list[Any] | None = None
    link: NewMessageLink | None = None
    notify: bool | None = None
    format: str | None = None

    def build_query_params(self) -> dict[str, Any]:
        """Query params: chat_id or user_id, disable_link_preview."""
        params: dict[str, Any] = {}
        if self.chat_id is not None:
            params["chat_id"] = self.chat_id
        if self.user_id is not None:
            params["user_id"] = self.user_id
        if self.disable_link_preview is not None:
            params["disable_link_preview"] = str(self.disable_link_preview).lower()
        return params

    def build_request_body(self) -> dict[str, Any] | None:
        """Body is the NewMessageBody fields."""
        body: dict[str, Any] = {}
        if self.text is not None:
            body["text"] = self.text
        if self.attachments is not None:
            body["attachments"] = self.attachments
        if self.link is not None:
            body["link"] = self.link.model_dump(exclude_none=True)
        if self.notify is not None:
            body["notify"] = self.notify
        if self.format is not None:
            body["format"] = self.format
        return body if body else None
