from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import MaxObject
from .linked_message import LinkedMessage
from .message_body import MessageBody
from .message_stat import MessageStat
from .recipient import Recipient
from .user import User

if TYPE_CHECKING:
    from ..methods.answer_callback import AnswerCallback
    from ..methods.edit_message import EditMessage
    from ..methods.send_message import SendMessage


class Message(MaxObject):
    """Message in MAX chat."""

    sender: User | None = None
    recipient: Recipient
    timestamp: int = 0
    link: LinkedMessage | None = None
    body: MessageBody
    stat: MessageStat | None = None
    url: str | None = None

    async def answer(
        self,
        text: str | None = None,
        attachments: list[Any] | None = None,
        notify: bool | None = None,
        format: str | None = None,
        disable_link_preview: bool | None = None,
        keyboard: Any | None = None,
        **kwargs: Any,
    ) -> Message:
        from ..methods.send_message import SendMessage
        from ..utils.keyboard import prepare_keyboard

        bot = self.bot
        if format is None and bot.default.parse_mode:
            format = bot.default.parse_mode
        if notify is None and bot.default.notify is not None:
            notify = bot.default.notify
        if disable_link_preview is None and bot.default.disable_link_preview is not None:
            disable_link_preview = bot.default.disable_link_preview
        attachments = prepare_keyboard(attachments, keyboard)

        chat_id = self.recipient.chat_id
        user_id = self.recipient.user_id if not chat_id else None

        return await SendMessage(
            chat_id=chat_id,
            user_id=user_id,
            text=text,
            attachments=attachments,
            notify=notify,
            format=format,
            disable_link_preview=disable_link_preview,
            **kwargs,
        ).as_(bot)

    async def reply(
        self,
        text: str | None = None,
        attachments: list[Any] | None = None,
        notify: bool | None = None,
        format: str | None = None,
        disable_link_preview: bool | None = None,
        keyboard: Any | None = None,
        **kwargs: Any,
    ) -> Message:
        from ..methods.send_message import SendMessage
        from ..types.new_message_link import NewMessageLink
        from ..utils.keyboard import prepare_keyboard

        bot = self.bot
        if format is None and bot.default.parse_mode:
            format = bot.default.parse_mode
        if notify is None and bot.default.notify is not None:
            notify = bot.default.notify
        if disable_link_preview is None and bot.default.disable_link_preview is not None:
            disable_link_preview = bot.default.disable_link_preview
        attachments = prepare_keyboard(attachments, keyboard)

        chat_id = self.recipient.chat_id
        user_id = self.recipient.user_id if not chat_id else None

        return await SendMessage(
            chat_id=chat_id,
            user_id=user_id,
            text=text,
            attachments=attachments,
            link=NewMessageLink(type="reply", mid=self.body.mid),
            notify=notify,
            format=format,
            disable_link_preview=disable_link_preview,
            **kwargs,
        ).as_(bot)

    async def edit_text(
        self,
        text: str | None = None,
        attachments: list[Any] | None = None,
        notify: bool | None = None,
        format: str | None = None,
        keyboard: Any | None = None,
        **kwargs: Any,
    ) -> bool:
        from ..methods.edit_message import EditMessage
        from ..utils.keyboard import prepare_keyboard

        bot = self.bot
        if format is None and bot.default.parse_mode:
            format = bot.default.parse_mode
        attachments = prepare_keyboard(attachments, keyboard)
        if attachments is None:
            attachments = []

        return await EditMessage(
            message_id=self.body.mid,
            text=text,
            attachments=attachments,
            notify=notify,
            format=format,
            **kwargs,
        ).as_(bot)
