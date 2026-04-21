from __future__ import annotations

import asyncio
import contextlib
import logging
import signal
import ssl
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from aiohttp import web

from maxgram import loggers
from maxgram.exceptions import MaxAPIError
from maxgram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    ip_filter_middleware,
    setup_application,
)
from maxgram.webhook.security import IPFilter

if TYPE_CHECKING:
    from maxgram.client.bot import Bot
    from maxgram.dispatcher.dispatcher import Dispatcher
    from maxgram.types.base import UNSET_TYPE


def _derive_path_from_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or "/"
    return path if path.startswith("/") else "/" + path


def _build_ssl_context(
    ssl_context: ssl.SSLContext | None,
    ssl_certfile: str | None,
    ssl_keyfile: str | None,
) -> ssl.SSLContext | None:
    if ssl_context is not None:
        return ssl_context
    if ssl_certfile and ssl_keyfile:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(ssl_certfile, ssl_keyfile)
        return ctx
    if ssl_certfile or ssl_keyfile:
        msg = "Both ssl_certfile and ssl_keyfile must be provided together"
        raise ValueError(msg)
    return None


def _coerce_ip_filter(ip_filter: IPFilter | Sequence[str] | None) -> IPFilter | None:
    if ip_filter is None:
        return None
    if isinstance(ip_filter, IPFilter):
        return ip_filter
    return IPFilter(ips=list(ip_filter))


@contextlib.contextmanager
def _try_install_orjson(bot: Bot) -> Any:
    try:
        import orjson
    except ImportError:
        yield False
        return

    original_loads = bot.session.json_loads
    original_dumps = bot.session.json_dumps

    def _dumps(obj: Any) -> str:
        return orjson.dumps(obj).decode("utf-8")

    bot.session.json_loads = orjson.loads
    bot.session.json_dumps = _dumps
    try:
        yield True
    finally:
        bot.session.json_loads = original_loads
        bot.session.json_dumps = original_dumps


def _install_subscription_hooks(
    dispatcher: Dispatcher,
    bot: Bot,
    *,
    url: str,
    secret: str | None,
    allowed_updates_ref: list[list[str] | None],
    drop_pending_updates: bool,
) -> None:
    async def _on_startup(**_: Any) -> None:
        if drop_pending_updates:
            with contextlib.suppress(MaxAPIError):
                await bot.delete_subscription(url=url)
        await bot.create_subscription(
            url=url,
            update_types=allowed_updates_ref[0],
            secret=secret,
        )
        loggers.webhook.info("Webhook subscription registered: %s", url)

    async def _on_shutdown(**_: Any) -> None:
        with contextlib.suppress(MaxAPIError):
            await bot.delete_subscription(url=url)
        loggers.webhook.info("Webhook subscription removed: %s", url)

    dispatcher.startup.register(_on_startup)
    dispatcher.shutdown.register(_on_shutdown)


async def run_webhook_async(
    dispatcher: Dispatcher,
    bot: Bot,
    *,
    url: str,
    secret: str | None = None,
    host: str = "0.0.0.0",
    port: int = 8080,
    path: str | None = None,
    allowed_updates: list[str] | UNSET_TYPE | None = None,
    drop_pending_updates: bool = False,
    register_subscription: bool = True,
    handle_in_background: bool = True,
    ssl_context: ssl.SSLContext | None = None,
    ssl_certfile: str | None = None,
    ssl_keyfile: str | None = None,
    ip_filter: IPFilter | Sequence[str] | None = None,
    handle_signals: bool = True,
    close_bot_session: bool = True,
    access_log: logging.Logger | bool = False,
    app: web.Application | None = None,
    **kwargs: Any,
) -> None:
    """Async entrypoint for webhook server. See `Dispatcher.run_webhook` for docs."""
    from maxgram.types.base import UNSET

    resolved_updates: list[str] | None
    if allowed_updates is UNSET or allowed_updates is None:
        resolved_updates = dispatcher.resolve_used_update_types() or None
    else:
        resolved_updates = list(allowed_updates)
    allowed_updates_ref: list[list[str] | None] = [resolved_updates]

    target_path = path or _derive_path_from_url(url)
    ssl_ctx = _build_ssl_context(ssl_context, ssl_certfile, ssl_keyfile)
    ip_filter_obj = _coerce_ip_filter(ip_filter)

    if app is None:
        app = web.Application()

    if ip_filter_obj is not None:
        app.middlewares.append(ip_filter_middleware(ip_filter_obj))

    if register_subscription:
        _install_subscription_hooks(
            dispatcher,
            bot,
            url=url,
            secret=secret,
            allowed_updates_ref=allowed_updates_ref,
            drop_pending_updates=drop_pending_updates,
        )

    handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        handle_in_background=handle_in_background,
        secret_token=secret,
        **kwargs,
    )
    handler.register(app, target_path)
    setup_application(app, dispatcher, **kwargs)

    stop_event = asyncio.Event()

    if handle_signals:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            with contextlib.suppress(NotImplementedError):
                loop.add_signal_handler(sig, stop_event.set)

    if isinstance(access_log, logging.Logger):
        runner_log: logging.Logger | None = access_log
    elif access_log is True:
        runner_log = loggers.webhook
    else:
        runner_log = None

    with _try_install_orjson(bot):
        runner = web.AppRunner(app, access_log=runner_log)
        await runner.setup()
        site = web.TCPSite(runner, host=host, port=port, ssl_context=ssl_ctx)
        await site.start()
        scheme = "https" if ssl_ctx is not None else "http"
        loggers.webhook.info(
            "Webhook server started on %s://%s:%s%s (public URL: %s)",
            scheme, host, port, target_path, url,
        )
        try:
            await stop_event.wait()
        finally:
            loggers.webhook.info("Stopping webhook server")
            await runner.cleanup()
            if close_bot_session:
                await bot.session.close()
