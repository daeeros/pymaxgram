from enum import Enum


class UpdateType(str, Enum):
    MESSAGE_CREATED = "message_created"
    MESSAGE_CALLBACK = "message_callback"
    BOT_STARTED = "bot_started"
