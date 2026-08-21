# Message

Модель сообщения MAX.

## Message

```python
class Message(MaxObject):
    sender: User | None = None
    recipient: Recipient
    timestamp: int = 0
    link: LinkedMessage | None = None
    body: MessageBody
    stat: MessageStat | None = None
    url: str | None = None
```

### Поля

| Поле | Тип | Описание |
| --- | --- | --- |
| `sender` | `User \| None` | Отправитель сообщения |
| `recipient` | `Recipient` | Получатель (чат или пользователь) |
| `timestamp` | `int` | Время отправки (Unix timestamp) |
| `link` | `LinkedMessage \| None` | Ссылка на другое сообщение (ответ/пересылка) |
| `body` | `MessageBody` | Тело сообщения (текст + вложения) |
| `stat` | `MessageStat \| None` | Статистика (просмотры для каналов) |
| `url` | `str \| None` | URL сообщения |

!!! warning "stat и url в апдейтах"
    Вопреки описанию в API-справочнике, во входящих апдейтах `message_created`
    поля `stat` и `url` **не заполняются** даже для постов в каналах — они
    возвращаются только в ответе на `POST /messages`. Определять канал следует
    по `recipient.chat_type`, см. свойство `is_channel_post`.

### Свойства

| Свойство | Тип | Описание |
| --- | --- | --- |
| `chat_type` | `str \| None` | Тип чата (`recipient.chat_type`) |
| `is_channel_post` | `bool` | Пост опубликован в канале |

```python
from maxgram.filters import ChannelPost

@router.message(ChannelPost())
async def on_channel_post(message, bot):
    # У постов канала sender is None - они публикуются от имени канала
    await message.reply("Комментарий от бота")
```

### Методы

```python
# Ответить в тот же чат
await message.answer(
    text: str | None = None,
    attachments: list | None = None,
    notify: bool | None = None,
    format: str | None = None,
    disable_link_preview: bool | None = None,
    keyboard: InlineKeyboardBuilder | InlineKeyboard | list | None = None,
) -> Message

# Ответить с цитированием
await message.reply(
    text: str | None = None,
    attachments: list | None = None,
    notify: bool | None = None,
    format: str | None = None,
    disable_link_preview: bool | None = None,
    keyboard: InlineKeyboardBuilder | InlineKeyboard | list | None = None,
) -> Message

# Удалить сообщение
await message.delete() -> bool

# Отредактировать текст
# Если attachments и keyboard не переданы — все вложения удаляются
await message.edit_text(
    text: str | None = None,
    attachments: list | None = None,
    notify: bool | None = None,
    format: str | None = None,
    keyboard: InlineKeyboardBuilder | InlineKeyboard | list | None = None,
) -> bool
```

## MessageBody

```python
class MessageBody(MaxObject):
    mid: str                                           # ID сообщения
    seq: int = 0                                       # Порядковый номер
    text: str | None = None                            # Текст
    attachments: list[AttachmentUnion] | None = None   # Вложения (типизированные)
    markup: list[MarkupElement] | None = None          # Разметка текста
```

`attachments` — это discriminated union, поэтому каждый элемент приходит сразу
как конкретный подкласс (`PhotoAttachment`, `VideoAttachment` и т.д.) без
ручного разбора `attachment.type`. Подробнее см. [Вложения](./attachments.md).

### Свойства html_text / md_text

`MessageBody` собирает готовый отформатированный текст из пары `text + markup`
с корректным учётом UTF-16 оффсетов (важно для эмодзи и суррогатных пар —
позиции в `MarkupElement` по спеке MAX API считаются в UTF-16 code units).

```python
@property
def html_text(self) -> str: ...

@property
def md_text(self) -> str: ...
```

| Тип markup | HTML | Markdown |
| --- | --- | --- |
| `strong` | `<b>…</b>` | `**…**` |
| `emphasized` | `<i>…</i>` | `*…*` |
| `monospaced` | `<code>…</code>` | `` `…` `` |
| `strikethrough` | `<s>…</s>` | `~~…~~` |
| `underline` | `<u>…</u>` | `++…++` |
| `link` | `<a href="url">…</a>` | `[…](url)` |
| `user_mention` | `<a href="…">…</a>` | `[…](…)` |

Текст между markup'ами в `html_text` автоматически экранируется (`&`, `<`, `>`).
Пересекающиеся (overlapping) элементы разметки пропускаются — остаётся только
первый по `from_pos`.

Пример:

```python
@router.message()
async def handler(message: Message, bot):
    # Вместо ручной сборки <b>, <i> — сразу готовая строка
    await message.answer(text=message.body.html_text, format="html")
```

### MarkupElement

Элемент разметки текста. MAX API возвращает разметку в виде массива элементов
с позицией и длиной. Позиции `from_pos` и `length` измеряются в UTF-16
code units — `MessageBody.html_text`/`md_text` учитывают это автоматически.

```python
from pydantic import Field

class MarkupElement(MaxObject):
    type: str                          # Тип разметки
    from_pos: int = Field(alias="from")  # Начало в тексте (UTF-16 code units)
    length: int                        # Длина (UTF-16 code units)
    url: str | None = None             # Только для link
    user_link: str | None = None       # Только для user_mention (@username)
    user_id: int | None = None         # Только для user_mention (ID)
```

Типы разметки (`MarkupType`):

| Тип | Enum | Описание |
| --- | --- | --- |
| `strong` | `MarkupType.STRONG` | Жирный |
| `emphasized` | `MarkupType.EMPHASIZED` | Курсив |
| `monospaced` | `MarkupType.MONOSPACED` | Моноширинный |
| `link` | `MarkupType.LINK` | Ссылка (+ поле `url`) |
| `strikethrough` | `MarkupType.STRIKETHROUGH` | Зачёркнутый |
| `underline` | `MarkupType.UNDERLINE` | Подчёркнутый |
| `user_mention` | `MarkupType.USER_MENTION` | Упоминание (+ `user_id`, `user_link`) |

Пример:

```python
@router.message()
async def handler(message: Message, bot):
    if message.body.markup:
        for el in message.body.markup:
            print(f"{el.type}: pos={el.from_pos}, len={el.length}")
            if el.type == "link":
                print(f"  url: {el.url}")
            if el.type == "user_mention":
                print(f"  user: {el.user_id} ({el.user_link})")
```

## MessageStat

```python
class MessageStat(MaxObject):
    views: int | None = None  # Количество просмотров
```

## LinkedMessage

Ссылка на другое сообщение (ответ или пересылка).

```python
class LinkedMessage(MaxObject):
    type: str                      # "forward" или "reply"
    sender: User | None = None     # Автор оригинала
    chat_id: int | None = None     # Чат оригинала
    message: MessageBody | None = None  # Тело оригинала
```

## Recipient

```python
class Recipient(MaxObject):
    chat_id: int | None = None     # ID чата
    chat_type: str | None = None   # Тип чата: "dialog" / "chat" / "channel"
    user_id: int | None = None     # ID пользователя (для ЛС)
```

| Свойство | Тип | Описание |
| --- | --- | --- |
| `is_channel` | `bool` | `chat_type == "channel"` |

## NewMessageBody

Тело для создания/редактирования сообщений.

```python
class NewMessageBody(MaxObject):
    text: str | None = None
    attachments: list[AttachmentRequest] | None = None
    link: NewMessageLink | None = None
    notify: bool | None = None
    format: str | None = None      # "html" или "markdown"
```

## NewMessageLink

```python
class NewMessageLink(MaxObject):
    type: str   # "reply" или "forward"
    mid: str    # ID сообщения
```

## Исходные файлы

- `maxgram/types/message.py`
- `maxgram/types/message_body.py`
- `maxgram/types/markup.py`
- `maxgram/types/message_stat.py`
- `maxgram/types/linked_message.py`
- `maxgram/types/recipient.py`
- `maxgram/types/new_message_body.py`
- `maxgram/types/new_message_link.py`
