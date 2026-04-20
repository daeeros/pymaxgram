from __future__ import annotations

from ..enums.chat_admin_permission import ChatAdminPermission
from .base import MaxObject


class ChatAdmin(MaxObject):
    """Admin assignment request."""

    user_id: int
    permissions: list[ChatAdminPermission] | None = None
    alias: str | None = None
