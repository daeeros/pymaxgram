from __future__ import annotations

from typing import Any

from .base import MaxObject


class VideoUrls(MaxObject):
    """Video playback/download URLs."""

    urls: dict[str, str] | None = None


class VideoInfo(MaxObject):
    """Video information returned by GET /videos/{token}."""

    token: str
    urls: VideoUrls | None = None
    thumbnail: Any | None = None
    width: int = 0
    height: int = 0
    duration: int = 0
