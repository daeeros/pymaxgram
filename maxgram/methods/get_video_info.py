from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import VideoInfo


class GetVideoInfo(MaxMethod[VideoInfo]):
    """GET /videos/{video_token} - Get video information."""

    __returning__: ClassVar[type] = VideoInfo
    __http_method__: ClassVar[str] = "GET"
    __api_path__: ClassVar[str] = "/videos/{video_token}"

    video_token: str
