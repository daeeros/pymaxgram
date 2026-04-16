from __future__ import annotations

from typing import Any, ClassVar

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
    from_: int | None = None
    to: int | None = None
    count: int | None = None

    def build_query_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if self.chat_id is not None:
            params["chat_id"] = self.chat_id
        if self.message_ids is not None:
            params["message_ids"] = ",".join(self.message_ids)
        if self.from_ is not None:
            params["from"] = self.from_
        if self.to is not None:
            params["to"] = self.to
        if self.count is not None:
            params["count"] = self.count
        return params
