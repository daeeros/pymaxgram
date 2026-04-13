import logging
from typing import TYPE_CHECKING, Any

from maxgram import loggers
from maxgram.methods import MaxMethod
from maxgram.methods.base import Response, MaxType

from .base import BaseRequestMiddleware, NextRequestMiddlewareType

if TYPE_CHECKING:
    from maxgram.client.bot import Bot

logger = logging.getLogger(__name__)


class RequestLogging(BaseRequestMiddleware):
    def __init__(self, ignore_methods: list[type[MaxMethod[Any]]] | None = None):
        """
        Middleware for logging outgoing requests

        :param ignore_methods: methods to ignore in logging middleware
        """
        self.ignore_methods = ignore_methods or []

    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[MaxType],
        bot: "Bot",
        method: MaxMethod[MaxType],
    ) -> Response[MaxType]:
        if type(method) not in self.ignore_methods:
            loggers.middlewares.info(
                "Make request with method=%r by bot id=%d",
                type(method).__name__,
                bot.id,
            )
        return await make_request(bot, method)
