from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod


class AnswerCallback(MaxMethod[bool]):
    """POST /answers - Respond to callback button press."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "POST"
    __api_path__: ClassVar[str] = "/answers"

    callback_id: str
    text: str | None = None
    attachments: list[Any] | None = None
    notification: str | None = None
    notify: bool | None = None
    format: str | None = None

    def build_query_params(self) -> dict[str, Any]:
        return {"callback_id": self.callback_id}

    def build_request_body(self) -> dict[str, Any] | None:
        body: dict[str, Any] = {}
        message_body: dict[str, Any] = {}
        if self.text is not None:
            message_body["text"] = self.text
        if self.attachments is not None:
            message_body["attachments"] = self.attachments
        if self.notify is not None:
            message_body["notify"] = self.notify
        if self.format is not None:
            message_body["format"] = self.format
        if message_body:
            body["message"] = message_body
        if self.notification is not None:
            body["notification"] = self.notification
        return body if body else None
