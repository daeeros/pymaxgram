# Прочие фильтры

## ExceptionTypeFilter

Фильтр ошибок по типу исключения.

```python
class ExceptionTypeFilter(Filter):
    def __init__(self, *exception_types: type[Exception]) -> None: ...
```

```python
@router.error(ExceptionTypeFilter(ValueError, TypeError))
async def handle(error, bot): ...
```

## ExceptionMessageFilter

Фильтр ошибок по тексту (regex).

```python
class ExceptionMessageFilter(Filter):
    def __init__(self, pattern: str | re.Pattern) -> None: ...
```

```python
@router.error(ExceptionMessageFilter(r"timeout|connection"))
async def handle(error, bot): ...
```

## ChatTypeFilter

Фильтр по типу чата, из которого пришло событие.

```python
class ChatTypeFilter(Filter):
    def __init__(self, *chat_types: str | ChatType) -> None: ...
```

Тип берётся из `recipient.chat_type`; для `Callback` и `Update` — из вложенного
сообщения, поэтому фильтр работает и на `@router.message()`, и на
`@router.message_callback()`.

```python
from maxgram.enums import ChatType
from maxgram.filters import ChatTypeFilter

@router.message(ChatTypeFilter(ChatType.DIALOG, ChatType.CHAT))
async def not_a_channel(message, bot): ...
```

## ChannelPost

Сокращение для `ChatTypeFilter(ChatType.CHANNEL)` — пропускает только посты,
опубликованные в канале.

```python
class ChannelPost(ChatTypeFilter):
    def __init__(self) -> None: ...
```

```python
from maxgram.filters import ChannelPost

@router.message(ChannelPost())
async def on_channel_post(message, bot):
    await message.reply("Комментарий от бота")
```

Чтобы получать посты канала, бот должен быть администратором канала с правами
`read_all_messages` и `write`. Собственные сообщения бота обратно как
`message_created` не приходят, поэтому зацикливания не возникает.

## MagicData

Фильтр по данным middleware через magic-filter.

```python
class MagicData(Filter):
    def __init__(self, rule: MagicFilter) -> None: ...
```

```python
from maxgram import F
from maxgram.filters import MagicData

@router.message(MagicData(F.event_from_user.is_bot == False))
async def humans_only(message, bot): ...
```

## Логические комбинаторы

```python
def and_f(*filters: Filter) -> _AndFilter
def or_f(*filters: Filter) -> _OrFilter
def invert_f(filter: Filter) -> _InvertFilter
```

- `and_f(A, B)` — все фильтры должны пройти
- `or_f(A, B)` — хотя бы один
- `invert_f(A)` — инверсия (эквивалент `~A`)

```python
from maxgram.filters import or_f, Command

@router.message(or_f(Command("help"), Command("start")))
async def handler(message, bot): ...
```

## Исходные файлы

- `maxgram/filters/chat_type.py`
- `maxgram/filters/exception.py`
- `maxgram/filters/magic_data.py`
- `maxgram/filters/logic.py`
