from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Generic,
    TypeVar,
)

from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import model_validator

from maxgram.client.context_controller import BotContextController
from maxgram.types.base import UNSET_TYPE

if TYPE_CHECKING:
    from ..client.bot import Bot

MaxType = TypeVar("MaxType", bound=Any)


class Response(BaseModel, Generic[MaxType]):
    success: bool = True
    message: str | None = None
    result: MaxType | None = None


class MaxMethod(BotContextController, BaseModel, Generic[MaxType], ABC):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @model_validator(mode="before")
    @classmethod
    def remove_unset(cls, values: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(values, dict):
            return values
        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}

    if TYPE_CHECKING:
        __returning__: ClassVar[Any]
        __http_method__: ClassVar[str]
        __api_path__: ClassVar[str]
    else:

        @property
        @abstractmethod
        def __returning__(self) -> type:
            pass

        @property
        @abstractmethod
        def __http_method__(self) -> str:
            pass

        @property
        @abstractmethod
        def __api_path__(self) -> str:
            pass

    def build_request_path(self) -> str:
        """Build the actual API path with path parameters substituted."""
        path = self.__api_path__
        data = self.model_dump(warnings=False, exclude_none=True)
        # Substitute path parameters like {chat_id}, {user_id}, etc.
        for key, value in data.items():
            placeholder = "{" + key + "}"
            if placeholder in path:
                path = path.replace(placeholder, str(value))
        return path

    def build_query_params(self) -> dict[str, Any]:
        """Build query parameters for GET/DELETE requests."""
        path = self.__api_path__
        data = self.model_dump(warnings=False, exclude_none=True)
        params = {}
        for key, value in data.items():
            placeholder = "{" + key + "}"
            if placeholder in path:
                continue  # skip path params
            if isinstance(value, list):
                params[key] = ",".join(str(v) for v in value)
            elif isinstance(value, bool):
                params[key] = str(value).lower()
            else:
                params[key] = value
        return params

    def build_request_body(self) -> dict[str, Any] | None:
        """Build JSON body for POST/PUT/PATCH requests."""
        if self.__http_method__ in ("GET", "DELETE"):
            return None
        path = self.__api_path__
        data = self.model_dump(warnings=False, exclude_none=True)
        body = {}
        for key, value in data.items():
            placeholder = "{" + key + "}"
            if placeholder in path:
                continue  # skip path params
            body[key] = value
        return body if body else None

    async def emit(self, bot: Bot) -> MaxType:
        return await bot(self)

    def __await__(self) -> Generator[Any, None, MaxType]:
        bot = self._bot
        if not bot:
            raise RuntimeError(
                "This method is not mounted to any bot instance, please call it explicitly "
                "with bot instance `await bot(method)`\n"
                "or mount method to a bot instance `method.as_(bot)` "
                "and then call it `await method`"
            )
        return self.emit(bot).__await__()
