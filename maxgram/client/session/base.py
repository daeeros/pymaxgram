from __future__ import annotations

import abc
import json
from collections.abc import AsyncGenerator, Callable
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Final

from pydantic import ValidationError
from typing_extensions import Self

from maxgram.client.max_api import PRODUCTION, MaxAPIServer
from maxgram.exceptions import (
    ClientDecodeError,
    MaxAPIError,
    MaxBadRequest,
    MaxConflictError,
    MaxForbiddenError,
    MaxNotFound,
    MaxRateLimitError,
    MaxServerError,
    MaxServiceUnavailable,
    MaxUnauthorizedError,
)
from .middlewares.manager import RequestMiddlewareManager

if TYPE_CHECKING:
    from types import TracebackType

    from maxgram.client.bot import Bot
    from maxgram.methods import MaxMethod, Response
    from maxgram.methods.base import MaxType
    from maxgram.types import MaxObject

_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]

DEFAULT_TIMEOUT: Final[float] = 60.0


class BaseSession(abc.ABC):
    """Base class for all HTTP sessions in maxgram for MAX API."""

    def __init__(
        self,
        api: MaxAPIServer = PRODUCTION,
        json_loads: _JsonLoads = json.loads,
        json_dumps: _JsonDumps = json.dumps,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.api = api
        self.json_loads = json_loads
        self.json_dumps = json_dumps
        self.timeout = timeout
        self.middleware = RequestMiddlewareManager()

    def check_response(
        self,
        bot: Bot,
        method: MaxMethod[MaxType],
        status_code: int,
        content: str,
    ) -> Any:
        """Check response and return parsed result."""
        try:
            json_data = self.json_loads(content)
        except Exception as e:
            msg = "Failed to decode object"
            raise ClientDecodeError(msg, e, content) from e

        # If HTTP status is OK
        if HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED:
            # For bool-returning methods (success/message pattern)
            if method.__returning__ is bool:
                if isinstance(json_data, dict) and "success" in json_data:
                    if json_data["success"]:
                        return True
                    description = json_data.get("message", "Unknown error")
                    raise MaxAPIError(method=method, message=description)
                return True

            # For object-returning methods - parse the response directly
            returning_type = method.__returning__
            try:
                if returning_type is list:
                    item_type = getattr(method, "__item_type__", None)
                    raw_list = json_data
                    if isinstance(json_data, dict):
                        # Extract marker for pagination if present
                        if hasattr(method, "marker") and "marker" in json_data:
                            method.marker = json_data["marker"]
                        for key in ("messages", "chats", "members", "updates", "subscriptions"):
                            if key in json_data:
                                raw_list = json_data[key]
                                break
                        else:
                            if "message" in json_data and isinstance(json_data["message"], dict):
                                raw_list = json_data["message"]
                    if item_type and isinstance(raw_list, list):
                        return [
                            item_type.model_validate(item, context={"bot": bot})
                            if isinstance(item, dict) else item
                            for item in raw_list
                        ]
                    return raw_list
                else:
                    # Single object responses
                    if isinstance(json_data, dict):
                        # Some endpoints wrap result in a key (e.g., POST /messages returns {message: ...})
                        if "message" in json_data and isinstance(json_data["message"], dict):
                            # Could be a Message-wrapped response (like POST /messages)
                            if returning_type.__name__ in ("Message",):
                                return returning_type.model_validate(
                                    json_data["message"], context={"bot": bot}
                                )
                        return returning_type.model_validate(json_data, context={"bot": bot})
                    return returning_type.model_validate(json_data, context={"bot": bot})
            except (ValidationError, AttributeError) as e:
                msg = "Failed to deserialize object"
                raise ClientDecodeError(msg, e, json_data) from e

        # Error responses
        description = "Unknown error"
        if isinstance(json_data, dict):
            description = json_data.get("message", json_data.get("description", str(json_data)))

        if status_code == HTTPStatus.BAD_REQUEST:
            raise MaxBadRequest(method=method, message=description)
        if status_code == HTTPStatus.UNAUTHORIZED:
            raise MaxUnauthorizedError(method=method, message=description)
        if status_code == HTTPStatus.FORBIDDEN:
            raise MaxForbiddenError(method=method, message=description)
        if status_code == HTTPStatus.NOT_FOUND:
            raise MaxNotFound(method=method, message=description)
        if status_code == HTTPStatus.CONFLICT:
            raise MaxConflictError(method=method, message=description)
        if status_code == HTTPStatus.TOO_MANY_REQUESTS:
            raise MaxRateLimitError(method=method, message=description)
        if status_code == HTTPStatus.SERVICE_UNAVAILABLE:
            raise MaxServiceUnavailable(method=method, message=description)
        if status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            raise MaxServerError(method=method, message=description)

        raise MaxAPIError(method=method, message=description)

    @abc.abstractmethod
    async def close(self) -> None:
        """Close client session."""

    @abc.abstractmethod
    async def make_request(
        self,
        bot: Bot,
        method: MaxMethod[MaxType],
        timeout: int | None = None,
    ) -> MaxType:
        """Make request to MAX API."""

    @abc.abstractmethod
    async def stream_content(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        """Stream reader."""
        yield b""

    async def __call__(
        self,
        bot: Bot,
        method: MaxMethod[MaxType],
        timeout: int | None = None,
    ) -> MaxType:
        middleware = self.middleware.wrap_middlewares(self.make_request, timeout=timeout)
        return await middleware(bot, method)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()
