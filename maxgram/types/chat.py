from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..enums.chat_type import ChatType
from .base import MaxObject
from .image import Image

if TYPE_CHECKING:
    from .message import Message
    from .user_with_photo import UserWithPhoto


class Chat(MaxObject):
    """MAX chat object."""

    chat_id: int
    type: str = "chat"
    status: str = "active"
    title: str | None = None
    icon: Image | None = None
    last_event_time: int = 0
    participants_count: int = 0
    owner_id: int | None = None
    participants: dict[str, Any] | None = None
    is_public: bool = False
    link: str | None = None
    description: str | None = None
    dialog_with_user: UserWithPhoto | None = None
    chat_message_id: str | None = None
    pinned_message: Message | None = None
    messages_count: int | None = None

    @property
    def is_channel(self) -> bool:
        """Whether this chat is a channel."""
        return self.type == ChatType.CHANNEL

    @property
    def is_dialog(self) -> bool:
        """Whether this chat is a one-to-one dialog."""
        return self.type == ChatType.DIALOG
