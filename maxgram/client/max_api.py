from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MaxAPIServer:
    """MAX API server configuration."""

    base: str = "https://platform-api.max.ru"

    def api_url(self, path: str) -> str:
        """Build full API URL from path."""
        return f"{self.base}{path}"

    @classmethod
    def from_base(cls, base: str) -> MaxAPIServer:
        base = base.rstrip("/")
        return cls(base=base)


PRODUCTION = MaxAPIServer()
