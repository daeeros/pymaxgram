from __future__ import annotations

from html import escape as _html_escape
from typing import Iterable

from .attachment import AttachmentUnion
from .base import MaxObject
from .markup import MarkupElement


def _utf16_index(text: str) -> list[int]:
    """Cumulative UTF-16 position for each Python character index.

    ``result[i]`` is the UTF-16 offset of ``text[i]``; ``result[-1]`` is the
    total UTF-16 length. Surrogate-pair characters (code point > U+FFFF) take
    two UTF-16 units but one Python char.
    """
    cum = [0]
    for ch in text:
        cum.append(cum[-1] + (2 if ord(ch) > 0xFFFF else 1))
    return cum


def _utf16_to_py(cum: list[int], pos: int) -> int:
    lo, hi = 0, len(cum) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if cum[mid] < pos:
            lo = mid + 1
        else:
            hi = mid
    return lo


def _html_tags(m: MarkupElement) -> tuple[str, str]:
    t = m.type
    if t == "strong":
        return "<b>", "</b>"
    if t == "emphasized":
        return "<i>", "</i>"
    if t == "monospaced":
        return "<code>", "</code>"
    if t == "strikethrough":
        return "<s>", "</s>"
    if t == "underline":
        return "<u>", "</u>"
    if t == "link":
        url = _html_escape(m.url or "", quote=True)
        return f'<a href="{url}">', "</a>"
    if t == "user_mention":
        if m.user_link:
            url = _html_escape(f"https://max.ru/{m.user_link.lstrip('@')}", quote=True)
        elif m.user_id is not None:
            url = f"max://user/{m.user_id}"
        else:
            return "", ""
        return f'<a href="{url}">', "</a>"
    return "", ""


def _md_wrap(m: MarkupElement, inner: str) -> str:
    t = m.type
    if t == "strong":
        return f"**{inner}**"
    if t == "emphasized":
        return f"*{inner}*"
    if t == "monospaced":
        return f"`{inner}`"
    if t == "strikethrough":
        return f"~~{inner}~~"
    if t == "underline":
        return f"++{inner}++"
    if t == "link":
        return f"[{inner}]({m.url or ''})"
    if t == "user_mention":
        if m.user_link:
            return f"[{inner}](https://max.ru/{m.user_link.lstrip('@')})"
        if m.user_id is not None:
            return f"[{inner}](max://user/{m.user_id})"
    return inner


def _render(text: str, markup: Iterable[MarkupElement], *, html: bool) -> str:
    if not text:
        return ""
    ordered = sorted(markup, key=lambda m: (m.from_pos, m.from_pos + m.length))
    if not ordered:
        return _html_escape(text) if html else text

    cum = _utf16_index(text)
    parts: list[str] = []
    i = 0
    for m in ordered:
        start = _utf16_to_py(cum, m.from_pos)
        end = _utf16_to_py(cum, m.from_pos + m.length)
        if start < i or end <= start:
            continue  # skip overlapping or empty ranges
        if start > i:
            parts.append(_html_escape(text[i:start]) if html else text[i:start])
        inner_raw = text[start:end]
        if html:
            open_t, close_t = _html_tags(m)
            parts.append(open_t + _html_escape(inner_raw) + close_t)
        else:
            parts.append(_md_wrap(m, inner_raw))
        i = end
    if i < len(text):
        parts.append(_html_escape(text[i:]) if html else text[i:])
    return "".join(parts)


class MessageBody(MaxObject):
    """Message body containing text and attachments."""

    mid: str
    seq: int = 0
    text: str | None = None
    attachments: list[AttachmentUnion] | None = None
    markup: list[MarkupElement] | None = None

    @property
    def html_text(self) -> str:
        """Return text with markup rendered as HTML tags.

        Offsets in ``markup`` are interpreted as UTF-16 code units, matching
        the MAX API spec. If markup entries overlap, later entries are dropped.
        """
        return _render(self.text or "", self.markup or [], html=True)

    @property
    def md_text(self) -> str:
        """Return text with markup rendered as MAX-flavored markdown.

        Uses ``**bold**``, ``*italic*``, ``~~strike~~``, ``++underline++``,
        `` `code` ``, ``[text](url)``. Offsets are UTF-16 code units.
        """
        return _render(self.text or "", self.markup or [], html=False)
