from .base import MaxObject


class BotCommand(MaxObject):
    """Bot command description."""

    name: str
    description: str
