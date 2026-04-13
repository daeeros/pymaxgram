from __future__ import annotations

from .base import MaxObject


class User(MaxObject):
    """MAX user object."""

    user_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    is_bot: bool = False
    last_activity_time: int | None = None
    name: str | None = None  # deprecated field

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def mention_html(self) -> str:
        return f'<a href="max://user/{self.user_id}">{self.full_name}</a>'

    @property
    def mention_md(self) -> str:
        return f"[{self.full_name}](max://user/{self.user_id})"

    async def get_profile_photo(
        self,
        chat_id: int,
        full_size: bool = True,
    ) -> bytes | None:
        """Download user's profile photo.

        Args:
            chat_id: Any chat where this user is a member.
            full_size: If True, download full-size avatar. Otherwise thumbnail.

        Returns:
            Photo bytes, or None if no avatar.
        """
        from ..methods.get_members import GetMembers

        members = await GetMembers(
            chat_id=chat_id,
            user_ids=[self.user_id],
        ).as_(self.bot)

        if not members:
            return None

        member = members[0]
        url = (
            getattr(member, "full_avatar_url", None) if full_size
            else getattr(member, "avatar_url", None)
        ) or getattr(member, "full_avatar_url", None) or getattr(member, "avatar_url", None)

        if not url:
            return None

        chunks = []
        async for chunk in self.bot.session.stream_content(url):
            chunks.append(chunk)
        return b"".join(chunks)

    async def get_profile_photo_url(
        self,
        chat_id: int,
        full_size: bool = True,
    ) -> str | None:
        """Get user's profile photo URL without downloading.

        Args:
            chat_id: Any chat where this user is a member.
            full_size: If True, return full-size URL. Otherwise thumbnail.

        Returns:
            Avatar URL string, or None if no avatar.
        """
        from ..methods.get_members import GetMembers

        members = await GetMembers(
            chat_id=chat_id,
            user_ids=[self.user_id],
        ).as_(self.bot)

        if not members:
            return None

        member = members[0]
        if full_size:
            return getattr(member, "full_avatar_url", None) or getattr(member, "avatar_url", None)
        return getattr(member, "avatar_url", None) or getattr(member, "full_avatar_url", None)
