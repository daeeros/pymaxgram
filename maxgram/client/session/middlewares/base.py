from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol

from maxgram.methods.base import MaxType

if TYPE_CHECKING:
    from maxgram.client.bot import Bot
    from maxgram.methods import Response, MaxMethod


class NextRequestMiddlewareType(Protocol[MaxType]):  # pragma: no cover
    async def __call__(
        self,
        bot: Bot,
        method: MaxMethod[MaxType],
    ) -> Response[MaxType]:
        pass


class RequestMiddlewareType(Protocol):  # pragma: no cover
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[MaxType],
        bot: Bot,
        method: MaxMethod[MaxType],
    ) -> Response[MaxType]:
        pass


class BaseRequestMiddleware(ABC):
    """
    Generic middleware class
    """

    @abstractmethod
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[MaxType],
        bot: Bot,
        method: MaxMethod[MaxType],
    ) -> Response[MaxType]:
        """
        Execute middleware

        :param make_request: Wrapped make_request in middlewares chain
        :param bot: bot for request making
        :param method: Request method (Subclass of :class:`maxgram.methods.base.MaxMethod`)

        :return: :class:`maxgram.methods.Response`
        """
