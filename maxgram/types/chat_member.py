from __future__ import annotations

from typing import Any

from pydantic import model_validator

from ..enums.chat_admin_permission import ChatAdminPermission
from .user_with_photo import UserWithPhoto

_KNOWN_PERMISSIONS = frozenset(p.value for p in ChatAdminPermission)


class ChatMember(UserWithPhoto):
    """Chat member with additional membership info."""

    last_access_time: int | None = None
    is_owner: bool = False
    is_admin: bool = False
    join_time: int | None = None
    permissions: list[ChatAdminPermission] | None = None
    alias: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _drop_unknown_permissions(cls, data: Any) -> Any:
        if isinstance(data, dict):
            perms = data.get("permissions")
            if isinstance(perms, list):
                filtered = [
                    p for p in perms
                    if not isinstance(p, str) or p in _KNOWN_PERMISSIONS
                ]
                if len(filtered) != len(perms):
                    data = {**data, "permissions": filtered}
        return data
