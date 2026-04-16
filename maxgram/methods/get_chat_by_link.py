from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import Chat


class GetChatByLink(MaxMethod[Chat]):
    """GET /chats/{chat_link} - Get chat by link."""

    __returning__: ClassVar[type] = Chat
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/chats/{chat_link}"

    chat_link: str
