from __future__ import annotations

from typing import Annotated, Any, Literal, Union

from pydantic import Field

from .base import MaxObject
from .button import ButtonUnion
from .user import User
from .video_info import VideoUrls


class PhotoAttachmentPayload(MaxObject):
    """Payload of an image attachment."""

    photo_id: int | None = None
    token: str | None = None
    url: str | None = None


class PhotoAttachmentRequestPayload(MaxObject):
    """Payload used when attaching an image to an outgoing message."""

    url: str | None = None
    token: str | None = None
    photos: dict[str, Any] | None = None


class VideoAttachmentPayload(MaxObject):
    """Payload of a video attachment."""

    token: str | None = None
    url: str | None = None


class AudioAttachmentPayload(MaxObject):
    """Payload of an audio attachment."""

    token: str | None = None
    url: str | None = None


class FileAttachmentPayload(MaxObject):
    """Payload of a file attachment."""

    token: str | None = None
    url: str | None = None


class StickerAttachmentPayload(MaxObject):
    """Payload of a sticker attachment."""

    url: str | None = None
    code: str | None = None


class ContactAttachmentPayload(MaxObject):
    """Payload of a contact attachment."""

    vcf_info: str | None = None
    max_info: User | None = None


class ShareAttachmentPayload(MaxObject):
    """Payload of a share attachment."""

    url: str | None = None
    token: str | None = None


class LocationAttachmentPayload(MaxObject):
    """Payload of a location attachment."""

    latitude: float | None = None
    longitude: float | None = None


class ButtonsPayload(MaxObject):
    """Payload of an inline-keyboard attachment."""

    buttons: list[list[ButtonUnion]] | None = None


class Attachment(MaxObject):
    """Base attachment type."""

    type: str
    payload: Any | None = None


class PhotoAttachment(Attachment):
    """Photo/image attachment."""

    type: Literal["image"] = "image"
    payload: PhotoAttachmentPayload | None = None


class VideoAttachment(Attachment):
    """Video attachment."""

    type: Literal["video"] = "video"
    payload: VideoAttachmentPayload | None = None
    urls: VideoUrls | None = None
    thumbnail: PhotoAttachmentPayload | None = None
    width: int | None = None
    height: int | None = None
    duration: int | None = None


class AudioAttachment(Attachment):
    """Audio attachment."""

    type: Literal["audio"] = "audio"
    payload: AudioAttachmentPayload | None = None
    transcription: str | None = None


class FileAttachment(Attachment):
    """File attachment."""

    type: Literal["file"] = "file"
    payload: FileAttachmentPayload | None = None
    filename: str | None = None
    size: int | None = None


class StickerAttachment(Attachment):
    """Sticker attachment."""

    type: Literal["sticker"] = "sticker"
    payload: StickerAttachmentPayload | None = None
    width: int | None = None
    height: int | None = None


class ContactAttachment(Attachment):
    """Contact attachment."""

    type: Literal["contact"] = "contact"
    payload: ContactAttachmentPayload | None = None


class InlineKeyboardAttachment(Attachment):
    """Inline keyboard attachment."""

    type: Literal["inline_keyboard"] = "inline_keyboard"
    payload: ButtonsPayload | None = None


class LocationAttachment(Attachment):
    """Location attachment."""

    type: Literal["location"] = "location"
    payload: LocationAttachmentPayload | None = None
    latitude: float | None = None
    longitude: float | None = None


class ShareAttachment(Attachment):
    """Share attachment."""

    type: Literal["share"] = "share"
    payload: ShareAttachmentPayload | None = None
    title: str | None = None
    description: str | None = None
    image_url: str | None = None


AttachmentUnion = Annotated[
    Union[
        PhotoAttachment,
        VideoAttachment,
        AudioAttachment,
        FileAttachment,
        StickerAttachment,
        ContactAttachment,
        InlineKeyboardAttachment,
        LocationAttachment,
        ShareAttachment,
    ],
    Field(discriminator="type"),
]
