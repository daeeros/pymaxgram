from typing import Any

from .text_decorations import html_decoration, markdown_decoration


def _join(*content: Any, sep: str = " ") -> str:
    return sep.join(map(str, content))


def text(*content: Any, sep: str = " ") -> str:
    return _join(*content, sep=sep)


def bold(*content: Any, sep: str = " ") -> str:
    return markdown_decoration.bold(_join(*content, sep=sep))


def hbold(*content: Any, sep: str = " ") -> str:
    return html_decoration.bold(html_decoration.quote(_join(*content, sep=sep)))


def italic(*content: Any, sep: str = " ") -> str:
    return markdown_decoration.italic(_join(*content, sep=sep))


def hitalic(*content: Any, sep: str = " ") -> str:
    return html_decoration.italic(html_decoration.quote(_join(*content, sep=sep)))


def code(*content: Any, sep: str = " ") -> str:
    return markdown_decoration.code(_join(*content, sep=sep))


def hcode(*content: Any, sep: str = " ") -> str:
    return html_decoration.code(html_decoration.quote(_join(*content, sep=sep)))


def underline(*content: Any, sep: str = " ") -> str:
    return markdown_decoration.underline(_join(*content, sep=sep))


def hunderline(*content: Any, sep: str = " ") -> str:
    return html_decoration.underline(html_decoration.quote(_join(*content, sep=sep)))


def strikethrough(*content: Any, sep: str = " ") -> str:
    return markdown_decoration.strikethrough(_join(*content, sep=sep))


def hstrikethrough(*content: Any, sep: str = " ") -> str:
    return html_decoration.strikethrough(html_decoration.quote(_join(*content, sep=sep)))


def link(title: str, url: str) -> str:
    return markdown_decoration.link(title, url)


def hlink(title: str, url: str) -> str:
    return html_decoration.link(html_decoration.quote(title), url)
