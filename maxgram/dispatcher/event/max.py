from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from maxgram.dispatcher.middlewares.manager import MiddlewareManager
from maxgram.exceptions import UnsupportedKeywordArgument

from .bases import UNHANDLED, MiddlewareType, SkipHandler
from .handler import CallbackType, FilterObject, HandlerObject

if TYPE_CHECKING:
    from maxgram.dispatcher.router import Router
    from maxgram.types import MaxObject


class MaxEventObserver:
    """Event observer for MAX events."""

    def __init__(self, router: Router, event_name: str) -> None:
        self.router: Router = router
        self.event_name: str = event_name

        self.handlers: list[HandlerObject] = []

        self.middleware = MiddlewareManager()
        self.outer_middleware = MiddlewareManager()

        self._handler = HandlerObject(callback=lambda: True, filters=[])

    def filter(self, *filters: CallbackType) -> None:
        if self._handler.filters is None:
            self._handler.filters = []
        self._handler.filters.extend([FilterObject(filter_) for filter_ in filters])

    def _resolve_middlewares(self) -> list[MiddlewareType[MaxObject]]:
        middlewares: list[MiddlewareType[MaxObject]] = []
        for router in reversed(tuple(self.router.chain_head)):
            observer = router.observers.get(self.event_name)
            if observer:
                middlewares.extend(observer.middleware)
        return middlewares

    def register(
        self,
        callback: CallbackType,
        *filters: CallbackType,
        **kwargs: Any,
    ) -> CallbackType:
        if kwargs:
            msg = (
                "Passing any additional keyword arguments to the registrar method "
                "is not supported.\n"
                f"Please remove the {set(kwargs.keys())} arguments from this call.\n"
            )
            raise UnsupportedKeywordArgument(msg)

        self.handlers.append(
            HandlerObject(
                callback=callback,
                filters=[FilterObject(filter_) for filter_ in filters],
            ),
        )

        return callback

    def wrap_outer_middleware(
        self,
        callback: Any,
        event: MaxObject,
        data: dict[str, Any],
    ) -> Any:
        wrapped_outer = self.middleware.wrap_middlewares(
            self.outer_middleware,
            callback,
        )
        return wrapped_outer(event, data)

    def check_root_filters(self, event: MaxObject, **kwargs: Any) -> Any:
        return self._handler.check(event, **kwargs)

    async def trigger(self, event: MaxObject, **kwargs: Any) -> Any:
        for handler in self.handlers:
            kwargs["handler"] = handler
            result, data = await handler.check(event, **kwargs)
            if result:
                kwargs.update(data)
                try:
                    wrapped_inner = self.outer_middleware.wrap_middlewares(
                        self._resolve_middlewares(),
                        handler.call,
                    )
                    return await wrapped_inner(event, kwargs)
                except SkipHandler:
                    continue

        return UNHANDLED

    def __call__(
        self,
        *filters: CallbackType,
        **kwargs: Any,
    ) -> Callable[[CallbackType], CallbackType]:
        def wrapper(callback: CallbackType) -> CallbackType:
            self.register(callback, *filters, **kwargs)
            return callback

        return wrapper
