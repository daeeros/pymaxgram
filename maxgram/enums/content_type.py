from enum import Enum


class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"
    STICKER = "sticker"
    CONTACT = "contact"
    LOCATION = "location"
    SHARE = "share"
    INLINE_KEYBOARD = "inline_keyboard"
