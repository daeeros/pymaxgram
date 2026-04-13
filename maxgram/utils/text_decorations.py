"""
Text decoration utilities for MAX API.

MAX supports Markdown and HTML formatting in messages.

Markdown:
  *italic* or _italic_
  **bold** or __bold__
  ~~strikethrough~~
  ++underline++
  `code`
  [text](url)
  [Name](max://user/user_id)

HTML:
  <i> or <em>
  <b> or <strong>
  <del> or <s>
  <ins> or <u>
  <pre> or <code>
  <a href="url">text</a>
"""
from __future__ import annotations

import html as html_module


class TextDecoration:
    """Simple text decoration helper for MAX messages."""

    def bold(self, text: str) -> str:
        raise NotImplementedError

    def italic(self, text: str) -> str:
        raise NotImplementedError

    def underline(self, text: str) -> str:
        raise NotImplementedError

    def strikethrough(self, text: str) -> str:
        raise NotImplementedError

    def code(self, text: str) -> str:
        raise NotImplementedError

    def link(self, text: str, url: str) -> str:
        raise NotImplementedError

    def user_mention(self, text: str, user_id: int) -> str:
        raise NotImplementedError


class HtmlDecoration(TextDecoration):
    def bold(self, text: str) -> str:
        return f"<b>{text}</b>"

    def italic(self, text: str) -> str:
        return f"<i>{text}</i>"

    def underline(self, text: str) -> str:
        return f"<u>{text}</u>"

    def strikethrough(self, text: str) -> str:
        return f"<s>{text}</s>"

    def code(self, text: str) -> str:
        return f"<code>{text}</code>"

    def link(self, text: str, url: str) -> str:
        return f'<a href="{url}">{text}</a>'

    def user_mention(self, text: str, user_id: int) -> str:
        return f'<a href="max://user/{user_id}">{text}</a>'

    @staticmethod
    def quote(text: str) -> str:
        return html_module.escape(text)


class MarkdownDecoration(TextDecoration):
    def bold(self, text: str) -> str:
        return f"**{text}**"

    def italic(self, text: str) -> str:
        return f"*{text}*"

    def underline(self, text: str) -> str:
        return f"++{text}++"

    def strikethrough(self, text: str) -> str:
        return f"~~{text}~~"

    def code(self, text: str) -> str:
        return f"`{text}`"

    def link(self, text: str, url: str) -> str:
        return f"[{text}]({url})"

    def user_mention(self, text: str, user_id: int) -> str:
        return f"[{text}](max://user/{user_id})"


html_decoration = HtmlDecoration()
markdown_decoration = MarkdownDecoration()
