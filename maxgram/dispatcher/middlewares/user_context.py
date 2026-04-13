from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from maxgram.dispatcher.middlewares.base import BaseMiddleware
from maxgram.types import Chat, MaxObject, Recipient, Update, User

EVENT_CONTEXT_KEY = "event_context"

EVENT_FROM_USER_KEY = "event_from_user"
EVENT_CHAT_KEY = "event_chat"


@dataclass(frozen=True)
class EventContext:
    chat_id: int | None = None
    user: User | None = None

    @property
    def user_id(self) -> int | None:
        return self.user.user_id if self.user else None


class UserContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[MaxObject, dict[str, Any]], Awaitable[Any]],
        event: MaxObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Update):
            msg = "UserContextMiddleware got an unexpected event type!"
            raise RuntimeError(msg)
        event_context = data[EVENT_CONTEXT_KEY] = self.resolve_event_context(event=event)

        if event_context.user is not None:
            data[EVENT_FROM_USER_KEY] = event_context.user
        if event_context.chat_id is not None:
            data[EVENT_CHAT_KEY] = event_context.chat_id

        return await handler(event, data)

    @classmethod
    def resolve_event_context(cls, event: Update) -> EventContext:
        """Resolve user and chat from MAX Update object."""
        if event.update_type in ("message_created", "message_edited"):
            if event.message:
                return EventContext(
                    chat_id=event.message.recipient.chat_id,
                    user=event.message.sender,
                )
        if event.update_type == "message_callback" and event.callback:
            chat_id = None
            if event.callback.message and event.callback.message.recipient:
                chat_id = event.callback.message.recipient.chat_id
            return EventContext(
                chat_id=chat_id,
                user=event.callback.user,
            )
        if event.update_type == "message_removed":
            return EventContext(
                chat_id=event.chat_id,
            )
        if event.update_type in (
            "bot_started", "bot_stopped",
            "bot_added", "bot_removed",
            "user_added", "user_removed",
            "chat_title_changed",
            "dialog_muted", "dialog_unmuted",
            "dialog_cleared", "dialog_removed",
        ):
            return EventContext(
                chat_id=event.chat_id,
                user=event.user,
            )
        return EventContext()
