from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from typing_extensions import NotRequired

if TYPE_CHECKING:
    from maxgram import Bot, Dispatcher, Router
    from maxgram.dispatcher.event.handler import HandlerObject
    from maxgram.dispatcher.middlewares.user_context import EventContext
    from maxgram.fsm.context import FSMContext
    from maxgram.fsm.storage.base import BaseStorage
    from maxgram.types import Chat, Update, User


class DispatcherData(TypedDict, total=False):
    """
    Dispatcher and bot related data.
    """

    dispatcher: Dispatcher
    """Instance of the Dispatcher from which the handler was called."""
    bot: Bot
    """Bot that received the update."""
    bots: NotRequired[list[Bot]]
    """List of all bots in the Dispatcher. Used only in polling mode."""
    event_update: Update
    """Update object that triggered the handler."""
    event_router: Router
    """Router that was used to find the handler."""
    handler: NotRequired[HandlerObject]
    """Handler object that was called.
    Available only in the handler itself and inner middlewares."""


class UserContextData(TypedDict, total=False):
    """
    Event context related data about user and chat.
    """

    event_context: EventContext
    """Event context object that contains user and chat data."""
    event_from_user: NotRequired[User]
    """User object that triggered the handler."""
    event_chat: NotRequired[Chat]
    """Chat object that triggered the handler.
    .. deprecated:: 3.5.0
        Use :attr:`event_context.chat` instead."""
    event_thread_id: NotRequired[int]
    """Thread ID of the chat that triggered the handler.
    .. deprecated:: 3.5.0
        Use :attr:`event_context.chat` instead."""
    event_business_connection_id: NotRequired[str]
    """Business connection ID of the chat that triggered the handler.
    .. deprecated:: 3.5.0
        Use :attr:`event_context.business_connection_id` instead."""


class FSMData(TypedDict, total=False):
    """
    FSM related data.
    """

    fsm_storage: BaseStorage
    """Storage used for FSM."""
    state: NotRequired[FSMContext]
    """Current state of the FSM."""
    raw_state: NotRequired[str | None]
    """Raw state of the FSM."""


class MiddlewareData(
    DispatcherData,
    UserContextData,
    FSMData,
    total=False,
):
    """
    Data passed to the handler by the middlewares.

    You can add your own data by extending this class.
    """
