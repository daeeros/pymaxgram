from .base import MaxObject


class NewMessageLink(MaxObject):
    """Link to an existing message (for reply or forward)."""

    type: str  # "reply" or "forward"
    mid: str
