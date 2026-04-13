import functools
from collections.abc import Callable, Sequence
from typing import Any, overload

from maxgram.dispatcher.event.bases import (
    MiddlewareEventType,
    MiddlewareType,
    NextMiddlewareType,
)
from maxgram.dispatcher.event.handler import CallbackType
from maxgram.types import MaxObject


class MiddlewareManager(Sequence[MiddlewareType[MaxObject]]):
    def __init__(self) -> None:
        self._middlewares: list[MiddlewareType[MaxObject]] = []

    def register(
        self,
        middleware: MiddlewareType[MaxObject],
    ) -> MiddlewareType[MaxObject]:
        self._middlewares.append(middleware)
        return middleware

    def unregister(self, middleware: MiddlewareType[MaxObject]) -> None:
        self._middlewares.remove(middleware)

    def __call__(
        self,
        middleware: MiddlewareType[MaxObject] | None = None,
    ) -> (
        Callable[[MiddlewareType[MaxObject]], MiddlewareType[MaxObject]]
        | MiddlewareType[MaxObject]
    ):
        if middleware is None:
            return self.register
        return self.register(middleware)

    @overload
    def __getitem__(self, item: int) -> MiddlewareType[MaxObject]:
        pass

    @overload
    def __getitem__(self, item: slice) -> Sequence[MiddlewareType[MaxObject]]:
        pass

    def __getitem__(
        self,
        item: int | slice,
    ) -> MiddlewareType[MaxObject] | Sequence[MiddlewareType[MaxObject]]:
        return self._middlewares[item]

    def __len__(self) -> int:
        return len(self._middlewares)

    @staticmethod
    def wrap_middlewares(
        middlewares: Sequence[MiddlewareType[MiddlewareEventType]],
        handler: CallbackType,
    ) -> NextMiddlewareType[MiddlewareEventType]:
        @functools.wraps(handler)
        def handler_wrapper(event: MaxObject, kwargs: dict[str, Any]) -> Any:
            return handler(event, **kwargs)

        middleware = handler_wrapper
        for m in reversed(middlewares):
            middleware = functools.partial(m, middleware)  # type: ignore[assignment]
        return middleware
