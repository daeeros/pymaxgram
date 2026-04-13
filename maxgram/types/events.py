"""Typed event classes for each MAX API update_type.

These are thin wrappers around Update that provide typed access
to fields specific to each event type. Used as type hints in handlers.
"""
from __future__ import annotations

from .update import Update
from .user import User


class BotStarted(Update):
    """bot_started: user started the bot."""
    chat_id: int
    user: User
    payload: str | None = None
    user_locale: str | None = None


class BotStopped(Update):
    """bot_stopped: user stopped the bot."""
    chat_id: int
    user: User
    user_locale: str | None = None


class BotAdded(Update):
    """bot_added: bot added to chat."""
    chat_id: int
    user: User
    is_channel: bool = False


class BotRemoved(Update):
    """bot_removed: bot removed from chat."""
    chat_id: int
    user: User
    is_channel: bool = False


class UserAdded(Update):
    """user_added: user added to chat."""
    chat_id: int
    user: User
    inviter_id: int | None = None
    is_channel: bool = False


class UserRemoved(Update):
    """user_removed: user removed from chat."""
    chat_id: int
    user: User
    admin_id: int | None = None
    is_channel: bool = False


class ChatTitleChanged(Update):
    """chat_title_changed: chat title was changed."""
    chat_id: int
    user: User
    title: str = ""


class MessageRemoved(Update):
    """message_removed: message was deleted."""
    message_id: str = ""
    chat_id: int = 0
    user_id: int = 0


class DialogMuted(Update):
    """dialog_muted: dialog notifications muted."""
    chat_id: int
    user: User
    muted_until: int = 0
    user_locale: str | None = None


class DialogUnmuted(Update):
    """dialog_unmuted: dialog notifications unmuted."""
    chat_id: int
    user: User
    user_locale: str | None = None


class DialogCleared(Update):
    """dialog_cleared: dialog was cleared."""
    chat_id: int
    user: User
    user_locale: str | None = None


class DialogRemoved(Update):
    """dialog_removed: dialog was removed."""
    chat_id: int
    user: User
    user_locale: str | None = None


# Mapping from update_type to event class
EVENT_TYPE_MAP: dict[str, type[Update]] = {
    "bot_started": BotStarted,
    "bot_stopped": BotStopped,
    "bot_added": BotAdded,
    "bot_removed": BotRemoved,
    "user_added": UserAdded,
    "user_removed": UserRemoved,
    "chat_title_changed": ChatTitleChanged,
    "message_removed": MessageRemoved,
    "dialog_muted": DialogMuted,
    "dialog_unmuted": DialogUnmuted,
    "dialog_cleared": DialogCleared,
    "dialog_removed": DialogRemoved,
}
