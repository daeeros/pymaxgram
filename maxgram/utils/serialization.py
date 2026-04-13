from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from maxgram import Bot
from maxgram.client.default import DefaultBotProperties
from maxgram.methods import MaxMethod
from maxgram.types import InputFile


def _get_fake_bot(default: DefaultBotProperties | None = None) -> Bot:
    if default is None:
        default = DefaultBotProperties()
    return Bot(token="42:Fake", default=default)


@dataclass
class DeserializedMaxObject:
    """
    Represents a dumped max object.

    :param data: The dumped data of the max object.
    :type data: Any
    :param files: The dictionary containing the file names as keys
        and the corresponding `InputFile` objects as values.
    :type files: dict[str, InputFile]
    """

    data: Any
    files: dict[str, InputFile]


def deserialize_max_object(
    obj: Any,
    default: DefaultBotProperties | None = None,
    include_api_method_name: bool = True,
) -> DeserializedMaxObject:
    """
    Deserialize max Object to JSON compatible Python object.

    :param obj: The object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized max object.
    """
    extends = {}
    if include_api_method_name and isinstance(obj, MaxMethod):
        extends["method"] = obj.__api_method__

    if isinstance(obj, BaseModel):
        obj = obj.model_dump(mode="python", warnings=False)

    # Fake bot is needed to exclude global defaults from the object.
    fake_bot = _get_fake_bot(default=default)

    files: dict[str, InputFile] = {}
    prepared = fake_bot.session.prepare_value(
        obj,
        bot=fake_bot,
        files=files,
        _dumps_json=False,
    )

    if isinstance(prepared, dict):
        prepared.update(extends)
    return DeserializedMaxObject(data=prepared, files=files)


def deserialize_max_object_to_python(
    obj: Any,
    default: DefaultBotProperties | None = None,
    include_api_method_name: bool = True,
) -> Any:
    """
    Deserialize max object to JSON compatible Python object excluding files.

    :param obj: The max object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized max object.
    """
    return deserialize_max_object(
        obj,
        default=default,
        include_api_method_name=include_api_method_name,
    ).data
