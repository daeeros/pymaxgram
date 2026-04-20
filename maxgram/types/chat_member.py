from __future__ import annotations

from ..enums.chat_admin_permission import ChatAdminPermission
from .user_with_photo import UserWithPhoto


class ChatMember(UserWithPhoto):
    """Chat member with additional membership info."""

    last_access_time: int | None = None
    is_owner: bool = False
    is_admin: bool = False
    join_time: int | None = None
    permissions: list[ChatAdminPermission] | None = None
    alias: str | None = None
