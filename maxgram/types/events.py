"""Typed event classes for each MAX API update_type.

These are thin wrappers around Update that provide typed access
to fields specific to each event type. Used as type hints in handlers.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import model_validator

from ..enums.chat_admin_permission import ChatAdminPermission
from .chat_member import drop_unknown_permissions
from .update import Update
from .user import User


class BotStarted(Update):
    """bot_started: user started the bot.

    Deep link payload available in `event.payload`.
    Use `event.deep_link()` to decode base64-encoded payload.
    """
    chat_id: int
    user: User
    payload: str | None = None
    user_locale: str | None = None

    def deep_link(self, *, decoder: Callable[[bytes], bytes] | None = None) -> str | None:
        """Decode deep link payload.

        Returns decoded payload string, or None if no payload.

        Args:
            decoder: Optional custom decoder (e.g. AES decryptor).
                     Without it, decodes base64url.

        Usage::

            # Plain deep link
            @router.bot_started(F.payload)
            async def on_start(event: BotStarted):
                link_name = event.payload  # raw payload string

            # Base64-encoded deep link
            @router.bot_started(F.payload)
            async def on_start(event: BotStarted):
                decoded = event.deep_link()  # base64url decoded

            # Custom encryption
            @router.bot_started(F.payload)
            async def on_start(event: BotStarted):
                decoded = event.deep_link(decoder=my_cryptor.decrypt)
        """
        if not self.payload:
            return None
        from ..utils.payload import decode_payload
        try:
            return decode_payload(self.payload, decoder=decoder)
        except Exception:
            return self.payload


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
    post_id: str | None = None


class CommentRemoved(Update):
    """comment_removed: comment under a channel post was deleted.

    Bot gets it only as a channel admin with ``read_all_messages``,
    and never for its own actions.
    """
    message_id: str = ""
    chat_id: int = 0
    user_id: int = 0
    post_id: str | None = None


class BotAdminPermissionsChanged(Update):
    """bot_admin_permissions_changed: bot's admin rights changed in a chat or channel.

    Delivered via webhook only - long polling doesn't get this update.
    """
    chat_id: int
    user_id: int
    bot_id: int
    is_channel: bool = False
    is_admin: bool = False
    permissions: list[ChatAdminPermission] | None = None

    @model_validator(mode="before")
    @classmethod
    def _drop_unknown_permissions(cls, data: Any) -> Any:
        return drop_unknown_permissions(data)


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
    "comment_removed": CommentRemoved,
    "bot_admin_permissions_changed": BotAdminPermissionsChanged,
    "dialog_muted": DialogMuted,
    "dialog_unmuted": DialogUnmuted,
    "dialog_cleared": DialogCleared,
    "dialog_removed": DialogRemoved,
}
