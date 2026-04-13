from __future__ import annotations

from .bot_command import BotCommand
from .user_with_photo import UserWithPhoto


class BotInfo(UserWithPhoto):
    """Bot information returned by GET /me."""

    commands: list[BotCommand] | None = None
