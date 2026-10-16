from __future__ import annotations

from .base import MaxObject
from .message_body import MessageBody
from .message_stat import MessageStat
from .recipient import Recipient
from .user import User


class CommentMessageBody(MessageBody):
    """Body of a comment. Same as ``MessageBody`` but comments never carry attachments."""


class CommentLinkedMessage(MaxObject):
    """Comment that this comment replies to."""

    type: str  # "reply" - comments can't be forwarded
    sender: User | None = None
    chat_id: int | None = None
    message: CommentMessageBody | None = None


class CommentMessage(MaxObject):
    """Comment under a channel post, as returned by the ``/messages/{id}/comments`` methods.

    Unlike ``Message`` it has no ``url`` and its body has no attachments.
    ``sender`` is ``None`` when the comment was posted on behalf of the channel.
    """

    sender: User | None = None
    recipient: Recipient
    timestamp: int = 0
    link: CommentLinkedMessage | None = None
    body: CommentMessageBody
    stat: MessageStat | None = None
