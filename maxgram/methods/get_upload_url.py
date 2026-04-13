from __future__ import annotations

from typing import ClassVar

from maxgram.methods.base import MaxMethod
from maxgram.types import UploadInfo


class GetUploadUrl(MaxMethod[UploadInfo]):
    """POST /uploads - Get file upload URL."""

    __returning__: ClassVar[type] = UploadInfo
    __http_method__: ClassVar[str] = "POST"
    __api_path__: ClassVar[str] = "/uploads"

    type: str  # image, video, audio, file
