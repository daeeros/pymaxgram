from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from maxgram.types import MaxObject

T = TypeVar("T")


class BaseMiddleware(ABC):
    """Generic middleware class."""

    @abstractmethod
    async def __call__(
        self,
        handler: Callable[[MaxObject, dict[str, Any]], Awaitable[Any]],
        event: MaxObject,
        data: dict[str, Any],
    ) -> Any:
        pass
