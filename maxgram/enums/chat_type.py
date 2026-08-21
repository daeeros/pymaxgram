from enum import Enum


class ChatType(str, Enum):
    """Type of a MAX chat.

    Used both by :attr:`maxgram.types.Chat.type` and by
    :attr:`maxgram.types.Recipient.chat_type`.
    """

    DIALOG = "dialog"
    CHAT = "chat"
    CHANNEL = "channel"
