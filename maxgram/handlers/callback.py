from abc import ABC

from maxgram.handlers.base import BaseHandler
from maxgram.types import Callback, Message, User


class CallbackHandler(BaseHandler[Callback], ABC):
    """Base class for callback handlers."""

    @property
    def from_user(self) -> User:
        return self.event.user

    @property
    def message(self) -> Message | None:
        return self.event.message
