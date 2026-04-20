from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import Field

from .base import MaxObject


class Button(MaxObject):
    """Base inline keyboard button."""

    type: str
    text: str


class CallbackButton(Button):
    """Callback button — sends ``message_callback`` event."""

    type: Literal["callback"] = "callback"
    text: str
    payload: str | None = None


class LinkButton(Button):
    """Link button — opens URL in a new tab."""

    type: Literal["link"] = "link"
    text: str
    url: str


class RequestContactButton(Button):
    """Request contact button — requests user's contact."""

    type: Literal["request_contact"] = "request_contact"
    text: str


class RequestGeoLocationButton(Button):
    """Request geo location button — requests user's location."""

    type: Literal["request_geo_location"] = "request_geo_location"
    text: str
    quick: bool | None = None


class OpenAppButton(Button):
    """Open app button — opens a mini app."""

    type: Literal["open_app"] = "open_app"
    text: str
    web_app: str | None = None
    contact_id: int | None = None
    payload: str | None = None


class MessageButton(Button):
    """Message button — sends button text as a message from the user."""

    type: Literal["message"] = "message"
    text: str


class ClipboardButton(Button):
    """Clipboard button — copies payload text to clipboard."""

    type: Literal["clipboard"] = "clipboard"
    text: str
    payload: str


ButtonUnion = Annotated[
    Union[
        CallbackButton,
        LinkButton,
        RequestContactButton,
        RequestGeoLocationButton,
        OpenAppButton,
        MessageButton,
        ClipboardButton,
    ],
    Field(discriminator="type"),
]
