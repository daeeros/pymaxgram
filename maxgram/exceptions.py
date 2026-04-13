from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from maxgram.methods.base import MaxMethod, MaxType


class MaxgramError(Exception):
    """Base exception for all maxgram errors."""


class DetailedMaxgramError(MaxgramError):
    """Base exception for all maxgram errors with detailed message."""

    url: str | None = None

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        message = self.message
        if self.url:
            message += f"\n(background on this error at: {self.url})"
        return message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"


class MaxAPIError(DetailedMaxgramError):
    """Base exception for all MAX API errors."""

    label: str = "MAX server says"

    def __init__(
        self,
        method: MaxMethod[MaxType],
        message: str,
    ) -> None:
        super().__init__(message=message)
        self.method = method

    def __str__(self) -> str:
        original_message = super().__str__()
        return f"{self.label} - {original_message}"


class MaxNetworkError(MaxAPIError):
    """Base exception for all MAX network errors."""

    label = "HTTP Client says"


class MaxBadRequest(MaxAPIError):
    """Exception raised when request is malformed (400)."""


class MaxUnauthorizedError(MaxAPIError):
    """Exception raised when bot token is invalid (401)."""


class MaxNotFound(MaxAPIError):
    """Exception raised when resource not found (404)."""


class MaxConflictError(MaxAPIError):
    """Exception raised on conflict (409)."""


class MaxForbiddenError(MaxAPIError):
    """Exception raised when bot has no permission (403)."""


class MaxRateLimitError(MaxAPIError):
    """Exception raised when rate limit exceeded (429)."""

    def __init__(
        self,
        method: MaxMethod[MaxType],
        message: str,
    ) -> None:
        description = f"Rate limit exceeded on method {type(method).__name__!r}"
        description += f"\nOriginal description: {message}"
        super().__init__(method=method, message=description)


class MaxServerError(MaxAPIError):
    """Exception raised when MAX server returns 5xx error."""


class MaxServiceUnavailable(MaxServerError):
    """Exception raised when MAX server is unavailable (503)."""


class DataNotDictLikeError(DetailedMaxgramError):
    """Exception raised when data is not dict-like."""


class UnsupportedKeywordArgument(DetailedMaxgramError):
    """Exception raised when a keyword argument is passed as filter."""


class ClientDecodeError(MaxgramError):
    """Exception raised when client can't decode response."""

    def __init__(self, message: str, original: Exception, data: Any) -> None:
        self.message = message
        self.original = original
        self.data = data

    def __str__(self) -> str:
        original_type = type(self.original)
        return (
            f"{self.message}\n"
            f"Caused from error: "
            f"{original_type.__module__}.{original_type.__name__}: {self.original}\n"
            f"Content: {self.data}"
        )
