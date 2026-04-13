from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, ClassVar

NodeType = Any


class Text(Iterable[NodeType]):
    """Simple text element that renders as HTML."""

    tag: ClassVar[str | None] = None

    __slots__ = ("_body", "_params")

    def __init__(self, *body: NodeType, **params: Any) -> None:
        self._body: tuple[NodeType, ...] = body
        self._params: dict[str, Any] = params

    def render(self) -> str:
        parts = []
        for node in self._body:
            if isinstance(node, Text):
                parts.append(node.render())
            else:
                parts.append(str(node))

        content = "".join(parts)

        if self.tag:
            return self._wrap(content)
        return content

    def _wrap(self, content: str) -> str:
        return f"<{self.tag}>{content}</{self.tag}>"

    def as_kwargs(self) -> dict[str, Any]:
        return {
            "text": self.render(),
            "format": "html",
        }

    def as_caption_kwargs(self) -> dict[str, Any]:
        return {
            "caption": self.render(),
            "format": "html",
        }

    def as_html(self) -> str:
        return self.render()

    def __add__(self, other: NodeType) -> Text:
        if isinstance(other, Text) and type(other) is type(self):
            return type(self)(*self, *other, **self._params)
        if type(self) is Text and isinstance(other, str):
            return type(self)(*self, other, **self._params)
        return Text(self, other)

    def __iter__(self) -> Iterator[NodeType]:
        yield from self._body

    def __str__(self) -> str:
        return self.render()

    def __repr__(self) -> str:
        body_repr = ", ".join(
            repr(item) if not isinstance(item, Text) else repr(item)
            for item in self._body
        )
        return f"{type(self).__name__}({body_repr})"


class Bold(Text):
    """Bold text element."""
    tag = "b"


class Italic(Text):
    """Italic text element."""
    tag = "i"


class Underline(Text):
    """Underline text element."""
    tag = "u"


class Strikethrough(Text):
    """Strikethrough text element."""
    tag = "s"


class Code(Text):
    """Inline code: <code>text</code>"""
    tag = "code"


class Pre(Text):
    """Preformatted code block: <pre>text</pre>"""
    tag = "pre"


class TextLink(Text):
    """Hyperlink: <a href="url">text</a>"""

    def __init__(self, *body: NodeType, url: str, **params: Any) -> None:
        super().__init__(*body, **params)
        self._url = url

    tag = "a"

    def render(self) -> str:
        parts = []
        for node in self._body:
            if isinstance(node, Text):
                parts.append(node.render())
            else:
                parts.append(str(node))
        content = "".join(parts)
        return f'<a href="{self._url}">{content}</a>'


class UserMention(Text):
    """User mention: <a href="max://user/user_id">Name</a>"""

    def __init__(self, *body: NodeType, user_id: int, **params: Any) -> None:
        super().__init__(*body, **params)
        self._user_id = user_id

    tag = "a"

    def render(self) -> str:
        parts = []
        for node in self._body:
            if isinstance(node, Text):
                parts.append(node.render())
            else:
                parts.append(str(node))
        content = "".join(parts)
        return f'<a href="max://user/{self._user_id}">{content}</a>'


def as_line(*items: NodeType, end: str = "\n", sep: str = " ") -> Text:
    """Wrap items into a single line."""
    if sep:
        nodes: list[Any] = []
        for item in items[:-1]:
            nodes.extend([item, sep])
        nodes.extend([items[-1], end])
    else:
        nodes = [*items, end]
    return Text(*nodes)


def as_list(*items: NodeType, sep: str = "\n") -> Text:
    """Wrap each element to separated lines."""
    nodes: list[Any] = []
    for item in items[:-1]:
        nodes.extend([item, sep])
    nodes.append(items[-1])
    return Text(*nodes)


def as_marked_list(*items: NodeType, marker: str = "- ") -> Text:
    """Wrap elements as marked list."""
    return as_list(*(Text(marker, item) for item in items))


def as_numbered_list(*items: NodeType, start: int = 1, fmt: str = "{}. ") -> Text:
    """Wrap elements as numbered list."""
    return as_list(*(Text(fmt.format(index), item) for index, item in enumerate(items, start)))


def as_section(title: NodeType, *body: NodeType) -> Text:
    """Wrap elements as section with title."""
    return Text(title, "\n", *body)


def as_marked_section(title: NodeType, *body: NodeType, marker: str = "- ") -> Text:
    """Wrap elements as section with marked list."""
    return as_section(title, as_marked_list(*body, marker=marker))


def as_numbered_section(
    title: NodeType, *body: NodeType, start: int = 1, fmt: str = "{}. ",
) -> Text:
    """Wrap elements as section with numbered list."""
    return as_section(title, as_numbered_list(*body, start=start, fmt=fmt))


def as_key_value(key: NodeType, value: NodeType) -> Text:
    """Wrap elements pair as key-value line."""
    return Text(Bold(key, ":"), " ", value)
