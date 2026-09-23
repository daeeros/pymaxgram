from __future__ import annotations

from typing import Any, ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types.bot_command import BotCommand


class EditBotCommands(MaxMethod[list[BotCommand]]):
    """PATCH /me/commands - Set bot commands (empty list deletes them)."""

    __returning__: ClassVar[type] = list
    __item_type__: ClassVar[type] = BotCommand
    __http_method__: ClassVar[str] = "PATCH"
    __api_path__: ClassVar[str] = "/me/commands"

    commands: list[BotCommand]

    def build_request_body(self) -> dict[str, Any] | None:
        return {
            "commands": [cmd.model_dump(exclude_none=True) for cmd in self.commands]
        }
