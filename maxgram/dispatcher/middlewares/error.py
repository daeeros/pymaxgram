from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, cast

from maxgram.dispatcher.event.bases import UNHANDLED, CancelHandler, SkipHandler
from maxgram.types import MaxObject, Update
from maxgram.types.error_event import ErrorEvent

from .base import BaseMiddleware

if TYPE_CHECKING:
    from maxgram.dispatcher.router import Router


class ErrorsMiddleware(BaseMiddleware):
    def __init__(self, router: Router):
        self.router = router

    async def __call__(
        self,
        handler: Callable[[MaxObject, dict[str, Any]], Awaitable[Any]],
        event: MaxObject,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except (SkipHandler, CancelHandler):  # pragma: no cover
            raise
        except Exception as e:
            response = await self.router.propagate_event(
                update_type="error",
                event=ErrorEvent(update=cast(Update, event), exception=e),
                **data,
            )
            if response is not UNHANDLED:
                return response
            raise
