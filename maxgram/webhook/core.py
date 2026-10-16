from __future__ import annotations

import asyncio
import contextlib
import secrets
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from maxgram import loggers
from maxgram.types import Update
from maxgram.utils.tasks import UPDATE_TASKS_DRAIN_TIMEOUT, drain_tasks

if TYPE_CHECKING:
    from maxgram.client.bot import Bot
    from maxgram.dispatcher.dispatcher import Dispatcher
    from maxgram.webhook.security import IPFilter


@dataclass
class WebhookResult:
    """Outcome of handling a webhook POST, framework-independent."""

    status: int
    body: dict[str, Any] = field(default_factory=dict)


class WebhookProcessor:
    """Framework-neutral webhook handler.

    Takes a parsed payload dict plus the incoming request's secret header and
    client IP, performs auth checks, and dispatches the update to the bot's
    dispatcher. Returns a :class:`WebhookResult` the HTTP-framework adapter can
    turn into its own response type.

    Adapters (aiohttp/FastAPI/Sanic) are thin shims that only do request/response
    marshalling; all behaviour lives here.
    """

    def __init__(
        self,
        dispatcher: Dispatcher,
        bot: Bot,
        *,
        secret_token: str | None = None,
        ip_filter: IPFilter | None = None,
        handle_in_background: bool = True,
        data: dict[str, Any] | None = None,
    ) -> None:
        self.dispatcher = dispatcher
        self.bot = bot
        self.secret_token = secret_token
        self.ip_filter = ip_filter
        self.handle_in_background = handle_in_background
        self.data = data or {}
        self._background_tasks: set[asyncio.Task[Any]] = set()

    def verify_secret(self, header_value: str) -> bool:
        if not self.secret_token:
            return True
        return secrets.compare_digest(header_value, self.secret_token)

    def check_ip(self, client_ip: str | None) -> bool:
        if self.ip_filter is None:
            return True
        return bool(client_ip) and client_ip in self.ip_filter

    async def process(
        self,
        payload: dict[str, Any],
        *,
        secret_header: str = "",
        client_ip: str | None = None,
    ) -> WebhookResult:
        if not self.check_ip(client_ip):
            return WebhookResult(status=401, body={"error": "Unauthorized IP"})
        if not self.verify_secret(secret_header):
            return WebhookResult(status=401, body={"error": "Unauthorized"})
        if self.handle_in_background:
            task = asyncio.create_task(self._feed_in_background(payload))
            self._background_tasks.add(task)
            task.add_done_callback(self._background_tasks.discard)
        else:
            await self.dispatcher.feed_webhook_update(
                self.bot, payload, **self.data
            )
        return WebhookResult(status=200, body={})

    async def _feed_in_background(self, payload: dict[str, Any]) -> None:
        """Process an update in a task that never ends with an exception.

        A failed task whose exception nobody retrieves gets logged again by
        ``Task.__del__`` ("Task exception was never retrieved") at garbage
        collection time, from whatever thread runs the collector. Inside a
        logging handler's worker thread that can deadlock the logger.
        """
        try:
            update = Update.model_validate(payload, context={"bot": self.bot})
        except Exception:
            update_type = payload.get("update_type") if isinstance(payload, dict) else None
            loggers.webhook.exception("Failed to parse webhook update type=%s", update_type)
            return
        with contextlib.suppress(Exception):  # already logged by the dispatcher
            await self.dispatcher.feed_webhook_update(self.bot, update, **self.data)

    async def drain(self, timeout: float = UPDATE_TASKS_DRAIN_TIMEOUT) -> None:
        """Wait for updates still being handled in the background. Call when the server stops."""
        await drain_tasks(
            self._background_tasks, timeout=timeout, logger=loggers.webhook, what="webhook updates",
        )

    async def close(self) -> None:
        await self.bot.session.close()
