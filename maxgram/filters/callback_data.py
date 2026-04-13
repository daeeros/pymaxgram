from __future__ import annotations

import types
import typing
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from typing import TYPE_CHECKING, Any, ClassVar, TypeVar
from uuid import UUID

from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from typing_extensions import Self

from maxgram.filters.base import Filter
from maxgram.types import Callback

if TYPE_CHECKING:
    from magic_filter import MagicFilter
    from pydantic.fields import FieldInfo

T = TypeVar("T", bound="CallbackData")

MAX_CALLBACK_LENGTH: int = 128

_UNION_TYPES = {typing.Union, types.UnionType}


class CallbackDataException(Exception):
    pass


class CallbackData(BaseModel):
    """
    Base class for callback data wrapper for MAX inline keyboards.

    Usage: `class MyCallback(CallbackData, prefix='my_cb'): ...`
    """

    if TYPE_CHECKING:
        __separator__: ClassVar[str]
        __prefix__: ClassVar[str]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if "prefix" not in kwargs:
            msg = (
                f"prefix required, usage example: "
                f"`class {cls.__name__}(CallbackData, prefix='my_callback'): ...`"
            )
            raise ValueError(msg)
        cls.__separator__ = kwargs.pop("sep", ":")
        cls.__prefix__ = kwargs.pop("prefix")
        if cls.__separator__ in cls.__prefix__:
            msg = (
                f"Separator symbol {cls.__separator__!r} can not be used "
                f"inside prefix {cls.__prefix__!r}"
            )
            raise ValueError(msg)
        super().__init_subclass__(**kwargs)

    def _encode_value(self, key: str, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, UUID):
            return value.hex
        if isinstance(value, bool):
            return str(int(value))
        if isinstance(value, (int, str, float, Decimal, Fraction)):
            return str(value)
        msg = (
            f"Attribute {key}={value!r} of type {type(value).__name__!r}"
            f" can not be packed to callback data"
        )
        raise ValueError(msg)

    def pack(self) -> str:
        result = [self.__prefix__]
        for key, field_info in self.model_fields.items():
            value = getattr(self, key)
            result.append(self._encode_value(key, value))
        callback_data = self.__separator__.join(result)
        if len(callback_data.encode()) > MAX_CALLBACK_LENGTH:
            msg = (
                f"Resulted callback data is too long! "
                f"len({callback_data!r}) > {MAX_CALLBACK_LENGTH}"
            )
            raise ValueError(msg)
        return callback_data

    @classmethod
    def unpack(cls, value: str) -> Self:
        prefix, *parts = value.split(cls.__separator__)
        if prefix != cls.__prefix__:
            msg = f"Bad prefix ({prefix!r} != {cls.__prefix__!r})"
            raise ValueError(msg)

        params = {}
        for (key, field_info), raw_value in zip(cls.model_fields.items(), parts):
            if raw_value == "" and _check_field_is_nullable(field_info):
                params[key] = None
            else:
                params[key] = raw_value
        return cls(**params)

    @classmethod
    def filter(cls, rule: MagicFilter | None = None) -> CallbackDataFilter:
        return CallbackDataFilter(callback_data=cls, rule=rule)


def _check_field_is_nullable(field_info: FieldInfo) -> bool:
    if field_info.default is None:
        return True
    if field_info.default is not PydanticUndefined and field_info.default is None:
        return True
    origin = typing.get_origin(field_info.annotation)
    if origin in _UNION_TYPES:
        args = typing.get_args(field_info.annotation)
        if type(None) in args:
            return True
    return False


class CallbackDataFilter(Filter):
    """Filter for CallbackData in MAX callbacks."""

    def __init__(
        self,
        *,
        callback_data: type[CallbackData],
        rule: MagicFilter | None = None,
    ) -> None:
        self.callback_data = callback_data
        self.rule = rule

    async def __call__(self, callback: Callback) -> bool | dict[str, Any]:
        if not isinstance(callback, Callback):
            return False
        # MAX uses 'payload' field instead of Telegram's 'data'
        if not callback.payload:
            return False
        try:
            decoded = self.callback_data.unpack(callback.payload)
        except (ValueError, TypeError):
            return False
        if self.rule is not None and not self.rule.resolve(decoded):
            return False
        return {"callback_data": decoded}
