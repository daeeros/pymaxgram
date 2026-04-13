from __future__ import annotations

from collections.abc import Generator
from typing import TYPE_CHECKING, Any, Final

from .event.bases import REJECTED, UNHANDLED
from .event.event import EventObserver
from .event.max import MaxEventObserver

if TYPE_CHECKING:
    from maxgram.types import MaxObject

INTERNAL_UPDATE_TYPES: Final[frozenset[str]] = frozenset({"update", "error"})


class Router:
    """
    Router can route update and nested update types like messages, callbacks, etc.
    """

    def __init__(self, *, name: str | None = None) -> None:
        self.name = name or hex(id(self))

        self._parent_router: Router | None = None
        self.sub_routers: list[Router] = []

        # MAX event observers (only 3 event types + error)
        self.message = MaxEventObserver(router=self, event_name="message_created")
        self.message_callback = MaxEventObserver(router=self, event_name="message_callback")
        self.bot_started = MaxEventObserver(router=self, event_name="bot_started")

        self.errors = self.error = MaxEventObserver(router=self, event_name="error")

        self.startup = EventObserver()
        self.shutdown = EventObserver()

        self.observers: dict[str, MaxEventObserver] = {
            "message_created": self.message,
            "message_callback": self.message_callback,
            "bot_started": self.bot_started,
            "error": self.errors,
        }

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name!r}"

    def __repr__(self) -> str:
        return f"<{self}>"

    def resolve_used_update_types(self, skip_events: set[str] | None = None) -> list[str]:
        handlers_in_use: set[str] = set()
        if skip_events is None:
            skip_events = set()
        skip_events = {*skip_events, *INTERNAL_UPDATE_TYPES}

        for router in self.chain_tail:
            for update_name, observer in router.observers.items():
                if observer.handlers and update_name not in skip_events:
                    handlers_in_use.add(update_name)

        return list(sorted(handlers_in_use))

    async def propagate_event(self, update_type: str, event: MaxObject, **kwargs: Any) -> Any:
        kwargs.update(event_router=self)
        observer = self.observers.get(update_type)

        async def _wrapped(max_event: MaxObject, **data: Any) -> Any:
            return await self._propagate_event(
                observer=observer,
                update_type=update_type,
                event=max_event,
                **data,
            )

        if observer:
            return await observer.wrap_outer_middleware(_wrapped, event=event, data=kwargs)
        return await _wrapped(event, **kwargs)

    async def _propagate_event(
        self,
        observer: MaxEventObserver | None,
        update_type: str,
        event: MaxObject,
        **kwargs: Any,
    ) -> Any:
        response = UNHANDLED
        if observer:
            result, data = await observer.check_root_filters(event, **kwargs)
            if not result:
                return UNHANDLED
            kwargs.update(data)

            response = await observer.trigger(event, **kwargs)
            if response is REJECTED:
                return UNHANDLED
            if response is not UNHANDLED:
                return response

        for router in self.sub_routers:
            response = await router.propagate_event(update_type=update_type, event=event, **kwargs)
            if response is not UNHANDLED:
                break

        return response

    @property
    def chain_head(self) -> Generator[Router, None, None]:
        router: Router | None = self
        while router:
            yield router
            router = router.parent_router

    @property
    def chain_tail(self) -> Generator[Router, None, None]:
        yield self
        for router in self.sub_routers:
            yield from router.chain_tail

    @property
    def parent_router(self) -> Router | None:
        return self._parent_router

    @parent_router.setter
    def parent_router(self, router: Router) -> None:
        if not isinstance(router, Router):
            msg = f"router should be instance of Router not {type(router).__name__!r}"
            raise ValueError(msg)
        if self._parent_router:
            msg = f"Router is already attached to {self._parent_router!r}"
            raise RuntimeError(msg)
        if self == router:
            msg = "Self-referencing routers is not allowed"
            raise RuntimeError(msg)

        parent: Router | None = router
        while parent is not None:
            if parent == self:
                msg = "Circular referencing of Router is not allowed"
                raise RuntimeError(msg)
            parent = parent.parent_router

        self._parent_router = router
        router.sub_routers.append(self)

    def include_routers(self, *routers: Router) -> None:
        if not routers:
            msg = "At least one router must be provided"
            raise ValueError(msg)
        for router in routers:
            self.include_router(router)

    def include_router(self, router: Router) -> Router:
        if not isinstance(router, Router):
            msg = f"router should be instance of Router not {type(router).__class__.__name__}"
            raise ValueError(msg)
        router.parent_router = self
        return router

    async def emit_startup(self, *args: Any, **kwargs: Any) -> None:
        kwargs.update(router=self)
        await self.startup.trigger(*args, **kwargs)
        for router in self.sub_routers:
            await router.emit_startup(*args, **kwargs)

    async def emit_shutdown(self, *args: Any, **kwargs: Any) -> None:
        kwargs.update(router=self)
        await self.shutdown.trigger(*args, **kwargs)
        for router in self.sub_routers:
            await router.emit_shutdown(*args, **kwargs)
