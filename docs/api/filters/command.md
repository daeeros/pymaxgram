# Command

## Command

Фильтр текстовых команд.

```python
class Command(Filter):
    def __init__(
        self,
        *commands: str | re.Pattern,
        prefix: str = "/",
        ignore_case: bool = False,
        ignore_mention: bool = False,
        magic: MagicFilter | None = None,
    ) -> None: ...
```

### Параметры

| Параметр | Тип | Описание |
| --- | --- | --- |
| `commands` | `str \| Pattern` | Имена команд (без префикса) или regex |
| `prefix` | `str` | Префикс (`"/"`) |
| `ignore_case` | `bool` | Без учёта регистра |
| `ignore_mention` | `bool` | Игнорировать @mention |
| `magic` | `MagicFilter \| None` | Дополнительный фильтр на `CommandObject` |

При совпадении инъектирует `command: CommandObject` в обработчик.

## CommandObject

```python
@dataclass
class CommandObject:
    prefix: str = "/"
    command: str = ""
    mention: str | None = None
    args: str | None = None
    regexp_match: re.Match | None = None
    magic_result: Any = None
```

## Исходный файл

`maxgram/filters/command.py`
