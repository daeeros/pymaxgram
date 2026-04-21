from __future__ import annotations

import asyncio
import contextlib
import logging
import ssl
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from maxgram import loggers
from maxgram.webhook.core import WebhookProcessor

if TYPE_CHECKING:
    from maxgram.client.bot import Bot
    from maxgram.dispatcher.dispatcher import Dispatcher
    from maxgram.webhook.security import IPFilter


def _extract_client_ip(request: Request) -> str | None:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    if request.client is not None:
        return request.client.host
    return None


async def run_fastapi_backend(
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

    @asynccontextmanager
    async def _lifespan(app: FastAPI):
        await dispatcher.emit_startup(**workflow_data)
        try:
            yield
        finally:
            await dispatcher.emit_shutdown(**workflow_data)
            if close_bot_session:
                await bot.session.close()

    app = FastAPI(lifespan=_lifespan, docs_url=None, redoc_url=None, openapi_url=None)

    processor = WebhookProcessor(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=secret,
        ip_filter=ip_filter,
        handle_in_background=handle_in_background,
        data=kwargs,
    )

    @app.post(path)
    async def _webhook(request: Request) -> JSONResponse:
        try:
            raw = await request.body()
            payload = bot.session.json_loads(raw) if raw else {}
        except Exception:
            return JSONResponse({"error": "Invalid JSON"}, status_code=400)
        result = await processor.process(
            payload,
            secret_header=request.headers.get("X-Max-Bot-Api-Secret", ""),
            client_ip=_extract_client_ip(request),
        )
        return JSONResponse(result.body, status_code=result.status)

    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        loop="auto",       # picks uvloop if installed (uvicorn[standard]), else asyncio
        http="auto",       # picks httptools if installed, else h11
        ws="none",         # MAX webhook doesn't use WS
        lifespan="on",
        access_log=bool(access_log),
        log_level="info" if access_log else "warning",
    )
    if ssl_context is not None:
        config.ssl = ssl_context

    server = uvicorn.Server(config)
    server.install_signal_handlers = lambda: None

    stop_event = asyncio.Event()
    _install_signal_handlers(stop_event, handle_signals)

    async def _wait_and_stop() -> None:
        await stop_event.wait()
        server.should_exit = True

    with _try_install_orjson(bot):
        scheme = "https" if ssl_context is not None else "http"
        loggers.webhook.info(
            "Webhook server (fastapi+uvicorn) started on %s://%s:%s%s (public URL: %s)",
            scheme, host, port, path, url,
        )
        stop_task = asyncio.create_task(_wait_and_stop())
        try:
            await server.serve()
        finally:
            stop_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await stop_task
            loggers.webhook.info("Stopping webhook server (fastapi+uvicorn)")
