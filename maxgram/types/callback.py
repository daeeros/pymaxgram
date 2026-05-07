from __future__ import annotations

from typing import Any

from .base import MaxObject
from .message import Message
from .user import User


class Callback(MaxObject):
    """Callback from inline keyboard button press."""

    callback_id: str
    timestamp: int = 0
    user: User
    payload: str | None = None
    message: Message | None = None

    async def answer(
        self,
        text: str | None = None,
        attachments: list[Any] | None = None,
        notification: str | None = None,
        notify: bool | None = None,
        format: str | None = None,
        keyboard: Any | None = None,
        clear_attachments: bool = True,
        **kwargs: Any,
    ) -> bool:
        from ..methods.answer_callback import AnswerCallback
        from ..utils.keyboard import prepare_keyboard

        bot = self.bot
        # Only apply default parse_mode when there's actual text to format
        if text is not None and format is None and bot.default.parse_mode:
            format = bot.default.parse_mode
        attachments = prepare_keyboard(attachments, keyboard)
        if attachments is None and clear_attachments:
            attachments = []

        return await AnswerCallback(
            callback_id=self.callback_id,
            text=text,
            attachments=attachments,
            notification=notification,
            notify=notify,
            format=format,
            **kwargs,
        ).as_(bot)

    async def edit_text(
        self,
        text: str | None = None,
        attachments: list[Any] | None = None,
        notify: bool | None = None,
        format: str | None = None,
        keyboard: Any | None = None,
        clear_attachments: bool = True,
        **kwargs: Any,
    ) -> bool:
        from ..methods.edit_message import EditMessage
        from ..utils.keyboard import prepare_keyboard

        if self.message is None:
            msg = "Cannot edit message: callback.message is None"
            raise RuntimeError(msg)

        bot = self.bot
        if format is None and bot.default.parse_mode:
            format = bot.default.parse_mode
        attachments = prepare_keyboard(attachments, keyboard)
        if attachments is None and clear_attachments:
            attachments = []

        return await EditMessage(
            message_id=self.message.body.mid,
            text=text,
            attachments=attachments,
            notify=notify,
            format=format,
            **kwargs,
        ).as_(bot)
