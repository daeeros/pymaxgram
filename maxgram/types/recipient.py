from __future__ import annotations

from ..enums.chat_type import ChatType
from .base import MaxObject


class Recipient(MaxObject):
    """Message recipient - can be a chat or a user."""

    chat_id: int | None = None
    chat_type: str | None = None
    user_id: int | None = None

    @property
    def is_channel(self) -> bool:
        """Whether the recipient is a channel."""
        return self.chat_type == ChatType.CHANNEL
