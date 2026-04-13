from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from maxgram.utils.dataclass import dataclass_kwargs


@dataclass(**dataclass_kwargs(slots=True, kw_only=True))
class DefaultBotProperties:
    """Default bot properties for MAX API."""

    parse_mode: str | None = None
    """Default parse mode for messages (markdown or html)."""
    disable_link_preview: bool | None = None
    """Disable link preview in messages."""
    notify: bool | None = None
    """Default notification setting."""

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item, None)
