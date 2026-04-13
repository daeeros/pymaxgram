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
    # message_created, message_callback, message_edited
    message: Message | None = None
    callback: Callback | None = None
    user_locale: str | None = None
    # bot_started, bot_stopped, bot_added, bot_removed, user_added, user_removed,
    # chat_title_changed, dialog_*
    chat_id: int | None = None
    user: User | None = None
    # bot_started
    payload: str | None = None
    # chat_title_changed
    title: str | None = None
    # user_added
    inviter_id: int | None = None
    # user_removed
    admin_id: int | None = None
    # bot_added, bot_removed, user_added, user_removed
    is_channel: bool | None = None
    # message_removed
    message_id: str | None = None
    user_id: int | None = None
    # dialog_muted
    muted_until: int | None = None

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
        """Return the typed event object based on update_type."""
        if self.update_type == "message_created":
            if self.message is not None:
                return self.message
        elif self.update_type == "message_edited":
            if self.message is not None:
                return self.message
            return self
        elif self.update_type == "message_callback":
            if self.callback is not None:
                return self.callback
        else:
            from .events import EVENT_TYPE_MAP

            event_cls = EVENT_TYPE_MAP.get(self.update_type)
            if event_cls is not None:
                return self._as_typed_event(event_cls)

        raise UpdateTypeLookupError(
            f"Unknown or unsupported update type: {self.update_type}"
        )

    def _as_typed_event(self, cls: type) -> Any:
        """Convert this Update to a typed event subclass."""
        data = self.model_dump()
        try:
            ctx = {"bot": self.bot}
        except Exception:
            ctx = None
        return cls.model_validate(data, context=ctx)
