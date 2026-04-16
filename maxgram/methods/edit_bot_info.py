from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import BotInfo
from maxgram.types.bot_command import BotCommand


class EditBotInfo(MaxMethod[BotInfo]):
    """PATCH /me - Edit bot information."""

    __returning__: ClassVar[type] = BotInfo
    __http_method__: ClassVar[str] = "PATCH"
    __api_path__: ClassVar[str] = "/me"

    name: str | None = None
    description: str | None = None
    commands: list[BotCommand] | None = None
    photo: dict[str, Any] | None = None

    def build_request_body(self) -> dict[str, Any] | None:
        body: dict[str, Any] = {}
        if self.name is not None:
            body["name"] = self.name
        if self.description is not None:
            body["description"] = self.description
        if self.commands is not None:
            body["commands"] = [
                cmd.model_dump(exclude_none=True) for cmd in self.commands
            ]
        if self.photo is not None:
            body["photo"] = self.photo
        return body if body else None
