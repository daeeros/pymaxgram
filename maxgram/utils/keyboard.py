from __future__ import annotations

from copy import deepcopy
from itertools import chain
from typing import TYPE_CHECKING, Any

from maxgram.filters.callback_data import CallbackData
from maxgram.types import Button
from maxgram.types.attachment_request import InlineKeyboardAttachmentRequest
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

    def button(
        self,
        text: str,
        type: str = "callback",
        payload: str | None = None,
        url: str | None = None,
        intent: str | None = None,
        callback_data: CallbackData | None = None,
    ) -> InlineKeyboardBuilder:
        """Add a button to the current row."""
        if callback_data is not None:
            type = "callback"
            if isinstance(callback_data, str):
                payload = callback_data
            else:
                payload = callback_data.pack()

        btn = Button(
            type=type,
            text=text,
            payload=payload,
            url=url,
            intent=intent,
        )

        if not self._markup:
            self._markup.append([])
        self._markup[-1].append(btn)
        return self

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
