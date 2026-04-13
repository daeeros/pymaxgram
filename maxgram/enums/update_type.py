from enum import Enum


class UpdateType(str, Enum):
    MESSAGE_CREATED = "message_created"
    MESSAGE_REMOVED = "message_removed"
    MESSAGE_EDITED = "message_edited"
    MESSAGE_CALLBACK = "message_callback"
    BOT_STARTED = "bot_started"
    BOT_ADDED = "bot_added"
    BOT_REMOVED = "bot_removed"
    USER_ADDED = "user_added"
    USER_REMOVED = "user_removed"
    CHAT_TITLE_CHANGED = "chat_title_changed"
