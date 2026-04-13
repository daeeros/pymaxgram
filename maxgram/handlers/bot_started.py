from abc import ABC

from maxgram.handlers.base import BaseHandler
from maxgram.types import Update, User


class BotStartedHandler(BaseHandler[Update], ABC):
    """Base class for bot_started event handlers."""

    @property
    def from_user(self) -> User | None:
        return self.event.user

    @property
    def chat_id(self) -> int | None:
        return self.event.chat_id
