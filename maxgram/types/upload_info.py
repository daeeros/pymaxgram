from __future__ import annotations

from .base import MaxObject


class UploadInfo(MaxObject):
    """Upload URL and token returned by POST /uploads."""

    url: str
    token: str | None = None
