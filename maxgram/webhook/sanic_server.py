from __future__ import annotations

import asyncio
import contextlib
import logging
import ssl
import uuid
from typing import TYPE_CHECKING, Any

from sanic import Sanic, response

from maxgram import loggers
from maxgram.webhook.core import WebhookProcessor

if TYPE_CHECKING:
    from maxgram.client.bot import Bot
    from maxgram.dispatcher.dispatcher import Dispatcher
    from maxgram.webhook.security import IPFilter


def _extract_client_ip(request: Any) -> str | None:
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.ip or None


async def run_sanic_backend(
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
    kwargs: dict[str, Any] | None = None,
) -> None:
    from maxgram.webhook.runner import _install_signal_handlers, _try_install_orjson

    kwargs = kwargs or {}
    workflow_data = {"dispatcher": dispatcher, **dispatcher.workflow_data, **kwargs}

    # Sanic requires a unique app name per process; uuid keeps it simple and stateless.
    app = Sanic(f"maxgram-webhook-{uuid.uuid4().hex[:8]}")
    app.config.ACCESS_LOG = bool(access_log)

    processor = WebhookProcessor(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=secret,
        ip_filter=ip_filter,
        handle_in_background=handle_in_background,
        data=kwargs,
    )

    @app.before_server_start
    async def _startup(app_: Any, loop_: Any) -> None:
        await dispatcher.emit_startup(**workflow_data)

    @app.before_server_stop
    async def _shutdown(app_: Any, loop_: Any) -> None:
        await dispatcher.emit_shutdown(**workflow_data)
        if close_bot_session:
            await bot.session.close()

    @app.post(path)
    async def _webhook(request: Any) -> Any:
        try:
            payload = bot.session.json_loads(request.body) if request.body else {}
        except Exception:
            return response.json({"error": "Invalid JSON"}, status=400)
        result = await processor.process(
            payload,
            secret_header=request.headers.get("X-Max-Bot-Api-Secret", ""),
            client_ip=_extract_client_ip(request),
        )
        return response.json(result.body, status=result.status)

    server_coro = app.create_server(
        host=host,
        port=port,
        return_asyncio_server=True,
        ssl=ssl_context,
        access_log=bool(access_log),
    )
    server = await server_coro
    if server is None:
        msg = "Sanic failed to create the asyncio server"
        raise RuntimeError(msg)

    await server.startup()
    await server.before_start()
    await server.start_serving()

    stop_event = asyncio.Event()
    _install_signal_handlers(stop_event, handle_signals)

    with _try_install_orjson(bot):
        scheme = "https" if ssl_context is not None else "http"
        loggers.webhook.info(
            "Webhook server (sanic) started on %s://%s:%s%s (public URL: %s)",
            scheme, host, port, path, url,
        )
        try:
            await stop_event.wait()
        finally:
            loggers.webhook.info("Stopping webhook server (sanic)")
            await server.before_stop()
            await server.close()
            with contextlib.suppress(asyncio.CancelledError):
                await server.wait_closed()
            await server.after_stop()
