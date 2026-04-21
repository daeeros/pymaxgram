from __future__ import annotations

import asyncio
import contextlib
import logging
import signal
import ssl
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from maxgram import loggers
from maxgram.exceptions import MaxAPIError
from maxgram.webhook.backends import WebhookBackend
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


def _install_signal_handlers(stop_event: asyncio.Event, handle_signals: bool) -> None:
    if not handle_signals:
        return
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        with contextlib.suppress(NotImplementedError):
            loop.add_signal_handler(sig, stop_event.set)


def _resolve_allowed_updates(
    dispatcher: Dispatcher,
    allowed_updates: list[str] | UNSET_TYPE | None,
) -> list[str] | None:
    from maxgram.types.base import UNSET

    if allowed_updates is UNSET or allowed_updates is None:
        return dispatcher.resolve_used_update_types() or None
    return list(allowed_updates)


def _normalize_backend(backend: WebhookBackend | str) -> WebhookBackend:
    if isinstance(backend, WebhookBackend):
        return backend
    try:
        return WebhookBackend(str(backend).lower())
    except ValueError as e:
        valid = ", ".join(b.value for b in WebhookBackend)
        msg = f"Unknown webhook backend: {backend!r} (valid: {valid})"
        raise ValueError(msg) from e


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
    app: Any = None,
    backend: WebhookBackend | str = WebhookBackend.AIOHTTP,
    **kwargs: Any,
) -> None:
    """Async entrypoint for webhook server. See :meth:`Dispatcher.run_webhook` for docs."""
    resolved_backend = _normalize_backend(backend)

    resolved_updates = _resolve_allowed_updates(dispatcher, allowed_updates)
    allowed_updates_ref: list[list[str] | None] = [resolved_updates]

    target_path = path or _derive_path_from_url(url)
    ssl_ctx = _build_ssl_context(ssl_context, ssl_certfile, ssl_keyfile)
    ip_filter_obj = _coerce_ip_filter(ip_filter)

    if register_subscription:
        _install_subscription_hooks(
            dispatcher,
            bot,
            url=url,
            secret=secret,
            allowed_updates_ref=allowed_updates_ref,
            drop_pending_updates=drop_pending_updates,
        )

    common = dict(
        dispatcher=dispatcher,
        bot=bot,
        url=url,
        secret=secret,
        host=host,
        port=port,
        path=target_path,
        handle_in_background=handle_in_background,
        ssl_context=ssl_ctx,
        ip_filter=ip_filter_obj,
        handle_signals=handle_signals,
        close_bot_session=close_bot_session,
        access_log=access_log,
        kwargs=kwargs,
    )

    if resolved_backend is WebhookBackend.AIOHTTP:
        await _run_aiohttp_backend(app=app, **common)
    elif resolved_backend is WebhookBackend.FASTAPI:
        try:
            from maxgram.webhook.fastapi_server import run_fastapi_backend
        except ImportError as e:
            msg = (
                "FastAPI webhook backend requires fastapi and uvicorn. "
                "Install with: pip install pymaxgram[fastapi]"
            )
            raise RuntimeError(msg) from e
        await run_fastapi_backend(**common)
    elif resolved_backend is WebhookBackend.SANIC:
        try:
            from maxgram.webhook.sanic_server import run_sanic_backend
        except ImportError as e:
            msg = (
                "Sanic webhook backend requires sanic. "
                "Install with: pip install pymaxgram[sanic]"
            )
            raise RuntimeError(msg) from e
        await run_sanic_backend(**common)


async def _run_aiohttp_backend(
    *,
    dispatcher: Dispatcher,
    bot: Bot,
    url: str,
    secret: str | None,
    host: str,
    port: int,
    path: str,
    handle_in_background: bool,
    ssl_context: ssl.SSLContext | None,
    ip_filter: IPFilter | None,
    handle_signals: bool,
    close_bot_session: bool,
    access_log: logging.Logger | bool,
    app: Any = None,
    kwargs: dict[str, Any] | None = None,
) -> None:
    from aiohttp import web

    from maxgram.webhook.aiohttp_server import (
        SimpleRequestHandler,
        ip_filter_middleware,
        setup_application,
    )

    kwargs = kwargs or {}

    if app is None:
        app = web.Application()

    if ip_filter is not None:
        app.middlewares.append(ip_filter_middleware(ip_filter))

    handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        handle_in_background=handle_in_background,
        secret_token=secret,
        **kwargs,
    )
    handler.register(app, path)
    setup_application(app, dispatcher, **kwargs)

    stop_event = asyncio.Event()
    _install_signal_handlers(stop_event, handle_signals)

    if isinstance(access_log, logging.Logger):
        runner_log: logging.Logger | None = access_log
    elif access_log is True:
        runner_log = loggers.webhook
    else:
        runner_log = None

    with _try_install_orjson(bot):
        runner = web.AppRunner(app, access_log=runner_log)
        await runner.setup()
        site = web.TCPSite(runner, host=host, port=port, ssl_context=ssl_context)
        await site.start()
        scheme = "https" if ssl_context is not None else "http"
        loggers.webhook.info(
            "Webhook server (aiohttp) started on %s://%s:%s%s (public URL: %s)",
            scheme, host, port, path, url,
        )
        try:
            await stop_event.wait()
        finally:
            loggers.webhook.info("Stopping webhook server (aiohttp)")
            await runner.cleanup()
            if close_bot_session:
                await bot.session.close()
