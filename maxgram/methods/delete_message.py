from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod


class DeleteMessage(MaxMethod[bool]):
    """DELETE /messages - Delete message."""

    __returning__: ClassVar[type] = bool
    __http_method__: ClassVar[str] = "DELETE"
    __api_path__: ClassVar[str] = "/messages"

    message_id: str

    def build_query_params(self) -> dict[str, Any]:
        return {"message_id": self.message_id}
