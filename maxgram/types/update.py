from __future__ import annotations

from typing import Any

from pydantic import model_validator

from .base import MaxObject
from .callback import Callback
from .message import Message
from .user import User


class UpdateTypeLookupError(Exception):
    """Raised when update type is unknown."""


class Update(MaxObject):
    """Incoming update from MAX API."""

    update_type: str
    timestamp: int = 0
    message: Message | None = None
    callback: Callback | None = None
    user: User | None = None
    chat_id: int | None = None
    user_locale: str | None = None
    payload: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _populate_callback_message(cls, values: dict[str, Any]) -> dict[str, Any]:
        """MAX API puts message at Update level for message_callback.
        Move it into callback so callback.message is always populated."""
        if not isinstance(values, dict):
            return values
        if (
            values.get("update_type") == "message_callback"
            and values.get("callback")
            and values.get("message")
        ):
            cb = values["callback"]
            if isinstance(cb, dict) and cb.get("message") is None:
                cb["message"] = values["message"]
        return values

    @property
    def event_type(self) -> str:
        """Return the update type string for dispatcher routing."""
        return self.update_type

    @property
    def event(self) -> Any:
        """Return the event object based on update_type."""
        if self.update_type == "message_created":
            if self.message is not None:
                return self.message
        elif self.update_type == "message_callback":
            if self.callback is not None:
                return self.callback
        elif self.update_type == "bot_started":
            return self

        raise UpdateTypeLookupError(
            f"Unknown or unsupported update type: {self.update_type}"
        )
