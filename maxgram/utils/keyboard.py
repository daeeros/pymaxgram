from __future__ import annotations

from copy import deepcopy
from itertools import chain
from typing import TYPE_CHECKING, Any

from maxgram.filters.callback_data import CallbackData
from maxgram.types import Button
from maxgram.types.attachment_request import InlineKeyboardAttachmentRequest
from maxgram.types.button import (
    CallbackButton,
    ClipboardButton,
    LinkButton,
    MessageButton,
    OpenAppButton,
    RequestContactButton,
    RequestGeoLocationButton,
)
from maxgram.types.inline_keyboard import InlineKeyboard

if TYPE_CHECKING:
    from collections.abc import Generator


class InlineKeyboardBuilder:
    """
    Builder for MAX inline keyboards.

    MAX keyboard constraints:
    - Up to 210 buttons total
    - Up to 30 rows
    - Up to 7 buttons per row
    """

    MAX_WIDTH = 7
    MAX_ROWS = 30
    MAX_BUTTONS = 210

    def __init__(self, markup: list[list[Button]] | None = None) -> None:
        self._markup: list[list[Button]] = markup or []

    @property
    def buttons(self) -> Generator[Button, None, None]:
        yield from chain.from_iterable(self._markup)

    def _append(self, btn: Button) -> InlineKeyboardBuilder:
        if not self._markup:
            self._markup.append([])
        self._markup[-1].append(btn)
        return self

    def callback(
        self,
        text: str,
        payload: str | None = None,
        *,
        callback_data: CallbackData | None = None,
    ) -> InlineKeyboardBuilder:
        """Add a callback button."""
        if callback_data is not None:
            if isinstance(callback_data, str):
                payload = callback_data
            else:
                payload = callback_data.pack()
        return self._append(CallbackButton(text=text, payload=payload))

    def link(self, text: str, url: str) -> InlineKeyboardBuilder:
        """Add a link button."""
        return self._append(LinkButton(text=text, url=url))

    def request_contact(self, text: str) -> InlineKeyboardBuilder:
        """Add a request contact button."""
        return self._append(RequestContactButton(text=text))

    def request_geo_location(
        self,
        text: str,
        *,
        quick: bool | None = None,
    ) -> InlineKeyboardBuilder:
        """Add a request geo location button."""
        return self._append(RequestGeoLocationButton(text=text, quick=quick))

    def open_app(
        self,
        text: str,
        *,
        web_app: str | None = None,
        contact_id: int | None = None,
        payload: str | None = None,
    ) -> InlineKeyboardBuilder:
        """Add an open app button."""
        return self._append(
            OpenAppButton(text=text, web_app=web_app, contact_id=contact_id, payload=payload),
        )

    def message(self, text: str) -> InlineKeyboardBuilder:
        """Add a message button."""
        return self._append(MessageButton(text=text))

    def clipboard(self, text: str, payload: str) -> InlineKeyboardBuilder:
        """Add a clipboard button."""
        return self._append(ClipboardButton(text=text, payload=payload))

    def row(self, *buttons: Button) -> InlineKeyboardBuilder:
        """Add a new row with optional buttons."""
        self._markup.append(list(buttons))
        return self

    def adjust(self, *sizes: int) -> InlineKeyboardBuilder:
        """Adjust rows to specified button counts."""
        all_buttons = list(self.buttons)
        self._markup = []

        idx = 0
        size_idx = 0
        while idx < len(all_buttons):
            size = sizes[min(size_idx, len(sizes) - 1)]
            self._markup.append(all_buttons[idx : idx + size])
            idx += size
            size_idx += 1

        return self

    def copy(self) -> InlineKeyboardBuilder:
        return InlineKeyboardBuilder(markup=deepcopy(self._markup))

    def export(self) -> list[list[Button]]:
        return self._markup

    def as_markup(self) -> InlineKeyboardAttachmentRequest:
        """Build the inline keyboard attachment for sending."""
        return InlineKeyboardAttachmentRequest.from_buttons(self._markup)


def prepare_keyboard(
    attachments: list[Any] | None,
    keyboard: InlineKeyboardBuilder | InlineKeyboard | list | None,
) -> list[Any] | None:
    """Convert keyboard parameter to attachments list."""
    if keyboard is None:
        return attachments

    if isinstance(keyboard, InlineKeyboardBuilder):
        kb_attachment = keyboard.as_markup()
    elif isinstance(keyboard, InlineKeyboard):
        kb_attachment = InlineKeyboardAttachmentRequest.from_buttons(keyboard.buttons)
    elif isinstance(keyboard, list):
        kb_attachment = InlineKeyboardAttachmentRequest.from_buttons(keyboard)
    else:
        msg = f"keyboard must be InlineKeyboardBuilder, InlineKeyboard, or list[list[Button]], got {type(keyboard).__name__}"
        raise TypeError(msg)

    kb_dict = kb_attachment.model_dump(mode="json", exclude_none=True)

    if attachments is None:
        return [kb_dict]
    return [*attachments, kb_dict]
