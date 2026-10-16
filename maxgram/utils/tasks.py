from __future__ import annotations

import asyncio
import logging
from collections.abc import Iterable
from typing import Any, Final

# How long a stopping polling loop / webhook server waits for updates still in handlers
UPDATE_TASKS_DRAIN_TIMEOUT: Final[float] = 15.0


async def drain_tasks(
    tasks: Iterable[asyncio.Task[Any]],
    *,
    timeout: float,
    logger: logging.Logger,
    what: str,
) -> None:
    """Wait for ``tasks`` to finish; cancel whatever is still running after ``timeout``.

    Used on shutdown so the bot session and app resources (DB pools etc.) are not
    closed under handlers that are still processing updates.
    """
    pending_tasks = {task for task in tasks if not task.done()}
    if not pending_tasks:
        return
    _, pending = await asyncio.wait(pending_tasks, timeout=timeout)
    if pending:
        logger.warning("Cancelling %d %s still running after %ss", len(pending), what, timeout)
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
