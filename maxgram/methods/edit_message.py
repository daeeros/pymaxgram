from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod


class EditMessage(MaxMethod[bool]):
    """PUT /messages - Edit message."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "PUT"
    __api_path__: ClassVar[str] = "/messages"

    message_id: str
    text: str | None = None
    attachments: list[Any] | None = None
    notify: bool | None = None
    format: str | None = None

    def build_query_params(self) -> dict[str, Any]:
        return {"message_id": self.message_id}

    def build_request_body(self) -> dict[str, Any] | None:
        body: dict[str, Any] = {}
        if self.text is not None:
            body["text"] = self.text
        if self.attachments is not None:
            body["attachments"] = self.attachments
        if self.notify is not None:
            body["notify"] = self.notify
        if self.format is not None:
            body["format"] = self.format
        return body if body else None
