# Update

Входящее обновление от MAX API. Поля зависят от `update_type`.

```python
class Update(MaxObject):
    # Общие
    update_type: str
    timestamp: int = 0
    # Сообщения
    message: Message | None = None
    callback: Callback | None = None
    user_locale: str | None = None
    # Чат/бот/пользователь
    chat_id: int | None = None
    user: User | None = None
    payload: str | None = None
    title: str | None = None
    is_channel: bool | None = None
    inviter_id: int | None = None
    admin_id: int | None = None
    message_id: str | None = None
    user_id: int | None = None
    post_id: str | None = None
    muted_until: int | None = None
    # bot_admin_permissions_changed
    bot_id: int | None = None
    is_admin: bool | None = None
    permissions: list[str] | None = None
```

!!! note "Пустые обновления"
    MAX иногда присылает `{"update_type": "message_created", "timestamp": ...}` без `message`.
    Диспетчер такие обновления молча пропускает (`EmptyUpdateError`, лог уровня DEBUG):
    outer-middleware на `dp.update` их видят, обработчики `message` — нет.

## Типы обновлений и их поля

**Сообщения:**

| `update_type` | Поля | Event |
| --- | --- | --- |
| `message_created` | `message`, `user_locale?` | `Message` |
| `message_callback` | `callback`, `message`, `user_locale?` | `Callback` |
| `message_edited` | `message` | `Message` |
| `message_removed` | `message_id`, `chat_id`, `user_id`, `post_id?` | `MessageRemoved` |

**Комментарии к постам** (бот — админ канала с `read_all_messages`, на свои действия событий нет):

| `update_type` | Поля | Event |
| --- | --- | --- |
| `comment_created` | `message` | `Message` |
| `comment_edited` | `message` | `Message` |
| `comment_removed` | `message_id`, `chat_id`, `user_id`, `post_id` | `CommentRemoved` |

**Бот:**

| `update_type` | Поля | Event |
| --- | --- | --- |
| `bot_started` | `chat_id`, `user`, `payload?`, `user_locale?` | `BotStarted` |
| `bot_stopped` | `chat_id`, `user`, `user_locale` | `BotStopped` |
| `bot_added` | `chat_id`, `user`, `is_channel` | `BotAdded` |
| `bot_removed` | `chat_id`, `user`, `is_channel` | `BotRemoved` |
| `bot_admin_permissions_changed` | `chat_id`, `user_id`, `bot_id`, `is_channel`, `is_admin`, `permissions?` | `BotAdminPermissionsChanged` |

`bot_admin_permissions_changed` приходит только через Webhook — в Long Polling его нет.

**Пользователи и чат:**

| `update_type` | Поля | Event |
| --- | --- | --- |
| `user_added` | `chat_id`, `user`, `inviter_id?`, `is_channel` | `UserAdded` |
| `user_removed` | `chat_id`, `user`, `admin_id?`, `is_channel` | `UserRemoved` |
| `chat_title_changed` | `chat_id`, `user`, `title` | `ChatTitleChanged` |

**Диалоги:**

| `update_type` | Поля | Event |
| --- | --- | --- |
| `dialog_muted` | `chat_id`, `user`, `muted_until`, `user_locale` | `DialogMuted` |
| `dialog_unmuted` | `chat_id`, `user`, `user_locale` | `DialogUnmuted` |
| `dialog_cleared` | `chat_id`, `user`, `user_locale` | `DialogCleared` |
| `dialog_removed` | `chat_id`, `user`, `user_locale` | `DialogRemoved` |

## Типизированные event-классы

Каждый тип события возвращает типизированный объект. Импорт из `maxgram.types`:

```python
from maxgram.types import (
    Message, Callback,                         # message_created, message_callback
    BotStarted, BotStopped,                    # bot lifecycle
    BotAdded, BotRemoved,                      # bot in chat
    UserAdded, UserRemoved,                    # user in chat
    ChatTitleChanged, MessageRemoved,           # chat events
    CommentRemoved,                            # comment_removed
    BotAdminPermissionsChanged,                # bot admin rights changed
    DialogMuted, DialogUnmuted,                # dialog events
    DialogCleared, DialogRemoved,
)
```

### Свойство `event`

- `message_created` -> `Message`
- `message_callback` -> `Callback`
- `message_edited` -> `Message`
- `message_removed` -> `MessageRemoved`
- `comment_created` -> `Message`
- `comment_edited` -> `Message`
- `comment_removed` -> `CommentRemoved`
- `bot_admin_permissions_changed` -> `BotAdminPermissionsChanged`
- `bot_started` -> `BotStarted`
- `bot_stopped` -> `BotStopped`
- `bot_added` -> `BotAdded`
- `bot_removed` -> `BotRemoved`
- `user_added` -> `UserAdded`
- `user_removed` -> `UserRemoved`
- `chat_title_changed` -> `ChatTitleChanged`
- `dialog_muted` -> `DialogMuted`
- `dialog_unmuted` -> `DialogUnmuted`
- `dialog_cleared` -> `DialogCleared`
- `dialog_removed` -> `DialogRemoved`

### BotStarted и Deep Links

`BotStarted` имеет метод `deep_link()` для декодирования payload:

```python
from maxgram.types import BotStarted

event.payload       # Сырая строка как пришла от MAX API
event.deep_link()   # Декодированная из base64url
```

| Метод | Описание |
| --- | --- |
| `event.payload` | Сырой payload (строка) |
| `event.deep_link()` | Декодировать base64url |
| `event.deep_link(decoder=fn)` | Кастомная расшифровка (AES и т.д.) |

Создание deep link:

```python
from maxgram.utils.payload import encode_payload

link = encode_payload("secret_data")  # "c2VjcmV0X2RhdGE"
# URL: https://max.ru/your_bot?start=c2VjcmV0X2RhdGE
```

## Примеры

```python
from maxgram import F
from maxgram.types import BotStarted, UserAdded, MessageRemoved, BotAdded

# Deep link
@router.bot_started(F.payload)
async def on_deep_link(event: BotStarted):
    decoded = event.deep_link()
    await event.answer(text=f"Ref: {decoded}")

# Regular start (no payload)
@router.bot_started()
async def on_start(event: BotStarted):
    await event.answer(text="Welcome!")

@router.bot_added()
async def on_bot_added(event: BotAdded, bot):
    print(f"Added to {'channel' if event.is_channel else 'chat'} {event.chat_id}")

@router.user_added()
async def on_user_added(event: UserAdded, bot):
    print(f"{event.user.first_name} joined chat {event.chat_id}")
    if event.inviter_id:
        print(f"Invited by {event.inviter_id}")

@router.message_removed()
async def on_removed(event: MessageRemoved, bot):
    print(f"Message {event.message_id} removed from {event.chat_id}")
```

## UpdateTypeLookupError

Выбрасывается при попытке получить `event` для неизвестного `update_type`.

## Исходный файл

`maxgram/types/update.py`
