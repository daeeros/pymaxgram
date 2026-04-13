from abc import ABC
from typing import cast

from maxgram.filters import CommandObject
from maxgram.handlers.base import BaseHandler, BaseHandlerMixin
from maxgram.types import Message, User


class MessageHandler(BaseHandler[Message], ABC):
    """Base class for message handlers."""

    @property
    def from_user(self) -> User | None:
        return self.event.sender

    @property
    def chat_id(self) -> int | None:
        return self.event.recipient.chat_id


class MessageHandlerCommandMixin(BaseHandlerMixin[Message]):
    @property
    def command(self) -> CommandObject | None:
        if "command" in self.data:
            return cast(CommandObject, self.data["command"])
        return None
