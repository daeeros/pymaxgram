from __future__ import annotations

from pydantic import Field

from .base import MaxObject


class MarkupElement(MaxObject):
    """Text markup element from MAX API.

    Types: strong, emphasized, monospaced, link, strikethrough, underline, user_mention.
    """

    type: str
    from_pos: int = Field(alias="from")
    length: int
    url: str | None = None
    user_link: str | None = None
    user_id: int | None = None
