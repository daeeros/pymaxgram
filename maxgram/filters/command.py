from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field, replace
from re import Match, Pattern
from typing import TYPE_CHECKING, Any, cast

from maxgram.filters.base import Filter
from maxgram.types import BotCommand, Message

if TYPE_CHECKING:
    from magic_filter import MagicFilter

    from maxgram import Bot

CommandPatternType = str | re.Pattern[str] | BotCommand


class CommandException(Exception):
    pass


class Command(Filter):
    """
    Filter for handling commands from text messages in MAX.
    """

    __slots__ = (
        "commands",
        "ignore_case",
        "ignore_mention",
        "magic",
        "prefix",
    )

    def __init__(
        self,
        *values: CommandPatternType,
        commands: Sequence[CommandPatternType] | CommandPatternType | None = None,
        prefix: str = "/",
        ignore_case: bool = False,
        ignore_mention: bool = False,
        magic: MagicFilter | None = None,
    ):
        if commands is None:
            commands = []
        if isinstance(commands, (str, re.Pattern, BotCommand)):
            commands = [commands]

        if not isinstance(commands, Iterable):
            msg = "Command filter only supports str, re.Pattern, BotCommand object or their Iterable"
            raise ValueError(msg)

        items = []
        for command in (*values, *commands):
            if isinstance(command, BotCommand):
                command = command.name
            if not isinstance(command, (str, re.Pattern)):
                msg = (
                    "Command filter only supports str, re.Pattern, BotCommand object"
                    " or their Iterable"
                )
                raise ValueError(msg)
            if ignore_case and isinstance(command, str):
                command = command.casefold()
            items.append(command)

        if not items:
            msg = "At least one command should be specified"
            raise ValueError(msg)

        self.commands = tuple(items)
        self.prefix = prefix
        self.ignore_case = ignore_case
        self.ignore_mention = ignore_mention
        self.magic = magic

    def __str__(self) -> str:
        return self._signature_to_string(
            *self.commands,
            prefix=self.prefix,
            ignore_case=self.ignore_case,
            ignore_mention=self.ignore_mention,
            magic=self.magic,
        )

    async def __call__(self, message: Message, bot: Bot) -> bool | dict[str, Any]:
        if not isinstance(message, Message):
            return False

        text = await self._strip_leading_bot_mention(message, bot)
        if not text:
            return False

        try:
            command = await self.parse_command(text=text, bot=bot)
        except CommandException:
            return False
        result = {"command": command}
        if command.magic_result and isinstance(command.magic_result, dict):
            result.update(command.magic_result)
        return result

    async def _strip_leading_bot_mention(
        self, message: Message, bot: Bot,
    ) -> str | None:
        body = message.body
        text = body.text if body else None
        if not text:
            return text

        if body and body.markup:
            leading = next(
                (m for m in body.markup
                 if m.type == "user_mention" and m.from_pos == 0),
                None,
            )
            if leading is not None:
                me = await bot.me()
                if leading.user_id is not None and leading.user_id == me.user_id:
                    return text[leading.length:].lstrip()
                return None
            return text

        if text.startswith("@"):
            first, _, rest = text.partition(" ")
            if len(first) > 1:
                me = await bot.me()
                uname = me.username
                if uname and first[1:].lower() == uname.lower():
                    return rest.lstrip()
                if first[1].isalnum() or first[1] == "_":
                    return None

        return text

    @classmethod
    def extract_command(cls, text: str) -> CommandObject:
        try:
            full_command, *args = text.split(maxsplit=1)
        except ValueError as e:
            msg = "not enough values to unpack"
            raise CommandException(msg) from e

        prefix, (command, _, mention) = full_command[0], full_command[1:].partition("@")
        return CommandObject(
            prefix=prefix,
            command=command,
            mention=mention or None,
            args=args[0] if args else None,
        )

    def validate_prefix(self, command: CommandObject) -> None:
        if command.prefix not in self.prefix:
            msg = "Invalid command prefix"
            raise CommandException(msg)

    async def validate_mention(self, bot: Bot, command: CommandObject) -> None:
        if command.mention and not self.ignore_mention:
            me = await bot.me()
            if me.username and command.mention.lower() != me.username.lower():
                msg = "Mention did not match"
                raise CommandException(msg)

    def validate_command(self, command: CommandObject) -> CommandObject:
        for allowed_command in cast(Sequence[CommandPatternType], self.commands):
            if isinstance(allowed_command, Pattern):
                result = allowed_command.match(command.command)
                if result:
                    return replace(command, regexp_match=result)

            command_name = command.command
            if self.ignore_case:
                command_name = command_name.casefold()

            if command_name == allowed_command:
                return command
        msg = "Command did not match pattern"
        raise CommandException(msg)

    async def parse_command(self, text: str, bot: Bot) -> CommandObject:
        command = self.extract_command(text)
        self.validate_prefix(command=command)
        await self.validate_mention(bot=bot, command=command)
        command = self.validate_command(command)
        command = self.do_magic(command=command)
        return command

    def do_magic(self, command: CommandObject) -> Any:
        if self.magic is None:
            return command
        result = self.magic.resolve(command)
        if not result:
            msg = "Rejected via magic filter"
            raise CommandException(msg)
        return replace(command, magic_result=result)


@dataclass(frozen=True)
class CommandObject:
    """Instance of this object always has command and its prefix."""

    prefix: str = "/"
    command: str = ""
    mention: str | None = None
    args: str | None = field(repr=False, default=None)
    regexp_match: Match[str] | None = field(repr=False, default=None)
    magic_result: Any | None = field(repr=False, default=None)

    @property
    def mentioned(self) -> bool:
        return bool(self.mention)

    @property
    def text(self) -> str:
        line = self.prefix + self.command
        if self.mention:
            line += "@" + self.mention
        if self.args:
            line += " " + self.args
        return line


