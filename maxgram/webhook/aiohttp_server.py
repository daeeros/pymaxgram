from __future__ import annotations

from abc import ABC, abstractmethod
from asyncio import Transport
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, cast

from aiohttp import web
from aiohttp.typedefs import Handler
from aiohttp.web_app import Application
from aiohttp.web_middlewares import middleware

from maxgram import Bot, Dispatcher, loggers
from maxgram.webhook.core import WebhookProcessor
from maxgram.webhook.security import IPFilter

if TYPE_CHECKING:
    pass


def setup_application(app: Application, dispatcher: Dispatcher, /, **kwargs: Any) -> None:
    """Configure startup-shutdown process for aiohttp app with dispatcher."""
    workflow_data = {
        "app": app,
        "dispatcher": dispatcher,
        **dispatcher.workflow_data,
        **kwargs,
    }

    async def on_startup(*a: Any, **kw: Any) -> None:
        await dispatcher.emit_startup(**workflow_data)

    async def on_shutdown(*a: Any, **kw: Any) -> None:
        await dispatcher.emit_shutdown(**workflow_data)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)


def check_ip(ip_filter: IPFilter, request: web.Request) -> tuple[str, bool]:
    if forwarded_for := request.headers.get("X-Forwarded-For", ""):
        forwarded_for, *_ = forwarded_for.split(",", maxsplit=1)
        return forwarded_for, forwarded_for in ip_filter

    if peer_name := cast(Transport, request.transport).get_extra_info("peername"):
        host, _ = peer_name
        return host, host in ip_filter

    return "", False


def ip_filter_middleware(
    ip_filter: IPFilter,
) -> Callable[[web.Request, Handler], Awaitable[Any]]:
    @middleware
    async def _ip_filter_middleware(request: web.Request, handler: Handler) -> Any:
        ip_address, accept = check_ip(ip_filter=ip_filter, request=request)
        if not accept:
            loggers.webhook.warning("Blocking request from an unauthorized IP: %s", ip_address)
            raise web.HTTPUnauthorized()
        return await handler(request)

    return _ip_filter_middleware


class BaseRequestHandler(ABC):
    def __init__(
        self,
        dispatcher: Dispatcher,
        handle_in_background: bool = False,
        **data: Any,
    ) -> None:
        self.dispatcher = dispatcher
        self.handle_in_background = handle_in_background
        self.data = data

    def register(self, app: Application, /, path: str, **kwargs: Any) -> None:
        app.on_shutdown.append(self._handle_close)
        app.router.add_route("POST", path, self.handle, **kwargs)

    async def _handle_close(self, *a: Any, **kw: Any) -> None:
        await self.close()

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def resolve_bot(self, request: web.Request) -> Bot:
        pass

    @abstractmethod
    def verify_secret(self, secret_token: str, bot: Bot) -> bool:
        pass

    async def handle(self, request: web.Request) -> web.Response:
        bot = await self.resolve_bot(request)
        if not self.verify_secret(
            request.headers.get("X-Max-Bot-Api-Secret", ""), bot
        ):
            return web.Response(body="Unauthorized", status=401)

        processor = WebhookProcessor(
            dispatcher=self.dispatcher,
            bot=bot,
            secret_token=None,  # already verified above via resolve_bot-scoped logic
            ip_filter=None,     # handled by ip_filter_middleware at app level
            handle_in_background=self.handle_in_background,
            data=self.data,
        )
        payload = await request.json(loads=bot.session.json_loads)
        result = await processor.process(payload)
        return web.json_response(
            result.body,
            status=result.status,
            dumps=bot.session.json_dumps,
        )

    __call__ = handle


class SimpleRequestHandler(BaseRequestHandler):
    def __init__(
        self,
        dispatcher: Dispatcher,
        bot: Bot,
        handle_in_background: bool = True,
        secret_token: str | None = None,
        **data: Any,
    ) -> None:
        super().__init__(dispatcher=dispatcher, handle_in_background=handle_in_background, **data)
        self.bot = bot
        self.secret_token = secret_token

    def verify_secret(self, secret_token: str, bot: Bot) -> bool:
        import secrets as _secrets
        if self.secret_token:
            return _secrets.compare_digest(secret_token, self.secret_token)
        return True

    async def close(self) -> None:
        await self.bot.session.close()

    async def resolve_bot(self, request: web.Request) -> Bot:
        return self.bot
