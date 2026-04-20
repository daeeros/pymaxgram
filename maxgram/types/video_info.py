from __future__ import annotations

from typing import TYPE_CHECKING

from .base import MaxObject

if TYPE_CHECKING:
    from .attachment import PhotoAttachmentPayload


class VideoUrls(MaxObject):
    """Video playback/download URLs, keyed by resolution."""

    mp4_1080: str | None = None
    mp4_720: str | None = None
    mp4_480: str | None = None
    mp4_360: str | None = None
    mp4_240: str | None = None
    mp4_144: str | None = None
    hls: str | None = None


class VideoInfo(MaxObject):
    """Video information returned by ``GET /videos/{token}``."""

    token: str
    urls: VideoUrls | None = None
    thumbnail: PhotoAttachmentPayload | None = None
    width: int = 0
    height: int = 0
    duration: int = 0
