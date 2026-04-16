# Класс Bot

Класс `Bot` — центральный HTTP-клиент для взаимодействия с MAX Bot API.

## Создание экземпляра

```python
from maxgram import Bot
from maxgram.client.default import DefaultBotProperties
from maxgram.enums import ParseMode

# Минимальная инициализация
bot = Bot(token="YOUR_BOT_TOKEN")

# С настройками по умолчанию
bot = Bot(
    token="YOUR_BOT_TOKEN",
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        disable_link_preview=True,
        notify=False,
    ),
)
```

## Конструктор

```python
Bot(
    token: str,
    session: Any | None = None,
    default: DefaultBotProperties | None = None,
    **kwargs: Any,
)
```

Параметры:

- **token** (`str`) — токен бота MAX Messenger. Обязательный параметр. Не может быть пустым.
- **session** (`Any | None`) — HTTP-сессия. По умолчанию создаётся `AiohttpSession()`.
- **default** (`DefaultBotProperties | None`) — настройки по умолчанию для отправки сообщений.
- **\*\*kwargs** — произвольные параметры, сохраняются как атрибуты экземпляра.

```python
# Пример с пользовательскими параметрами
bot = Bot(
    token="TOKEN",
    db=database_pool,
    config=app_config,
)
print(bot.db)      # database_pool
print(bot.config)  # app_config
```

## Свойства

| Свойство | Тип | Описание |
| --- | --- | --- |
| `token` | `str` | Токен бота (только чтение) |
| `id` | `int \| None` | ID бота. Доступен после вызова `get_me()` |
| `username` | `str \| None` | Username бота. Доступен после вызова `get_me()` |
| `session` | `BaseSession` | HTTP-сессия для выполнения запросов |
| `default` | `DefaultBotProperties` | Настройки по умолчанию |

## Методы: информация о боте

### get_me

```python
await bot.get_me() -> BotInfo
```

Возвращает информацию о боте. Результат кэшируется в свойстве `me()`.

### me

```python
await bot.me() -> BotInfo
```

Кэшированная версия `get_me()`. При первом вызове делает запрос к API,
при последующих возвращает закэшированный результат.

### edit_info

```python
await bot.edit_info(
    name: str | None = None,
    description: str | None = None,
    commands: list[BotCommand] | None = None,
    photo: dict | None = None,
) -> BotInfo
```

Изменяет информацию о боте (`PATCH /me`). Передавайте только те поля, которые нужно обновить.

### set_commands

```python
await bot.set_commands(commands: list[BotCommand]) -> BotInfo
```

Устанавливает список команд бота. Шорткат для `edit_info(commands=...)`.

```python
from maxgram.types import BotCommand

await bot.set_commands([
    BotCommand(name="start", description="Запуск бота"),
    BotCommand(name="help", description="Справка"),
])
```

### delete_commands

```python
await bot.delete_commands() -> BotInfo
```

Удаляет все команды бота.

## Методы: чаты

### get_chats

```python
await bot.get_chats(
    count: int | None = None,
    marker: int | None = None,
) -> list[Chat]
```

Получает список чатов бота.

- **count** — максимальное количество чатов
- **marker** — маркер для пагинации

### get_chat

```python
await bot.get_chat(chat_id: int) -> Chat
```

Получает информацию о конкретном чате по ID.

### get_chat_by_link

```python
await bot.get_chat_by_link(chat_link: str) -> Chat
```

Получает информацию о чате по ссылке.

### edit_chat

```python
await bot.edit_chat(
    chat_id: int,
    title: str | None = None,
    icon: dict[str, Any] | None = None,
    pin: str | None = None,
    notify: bool | None = None,
) -> Chat
```

Редактирует параметры чата. Возвращает обновлённый объект `Chat`.

### delete_chat

```python
await bot.delete_chat(chat_id: int) -> bool
```

Удаляет чат.

## Методы: сообщения

### send_message

```python
await bot.send_message(
    chat_id: int | None = None,
    user_id: int | None = None,
    text: str | None = None,
    attachments: list[Any] | None = None,
    link: Any | None = None,
    notify: bool | None = None,
    format: str | None = None,
    disable_link_preview: bool | None = None,
) -> Message
```

Отправляет сообщение. Нужно указать `chat_id` или `user_id`.

- **chat_id** — ID чата для отправки
- **user_id** — ID пользователя для отправки в личку
- **text** — текст сообщения
- **attachments** — список вложений (клавиатуры, файлы и т.д.)
- **link** — ссылка на другое сообщение (для ответа/пересылки)
- **notify** — отправлять уведомление (`True`/`False`)
- **format** — формат текста: `"html"` или `"markdown"`
- **disable_link_preview** — отключить превью ссылок

### edit_message

```python
await bot.edit_message(
    message_id: str,
    text: str | None = None,
    attachments: list[Any] | None = None,
    notify: bool | None = None,
    format: str | None = None,
) -> bool
```

Редактирует существующее сообщение.

### delete_message

```python
await bot.delete_message(message_id: str) -> bool
```

Удаляет сообщение.

### get_messages

```python
await bot.get_messages(
    chat_id: int | None = None,
    message_ids: list[str] | None = None,
    from_: int | None = None,
    to: int | None = None,
    count: int | None = None,
) -> list[Message]
```

Получает список сообщений из чата. `from_` и `to` — фильтрация по времени (Unix ms).

### get_message_by_id

```python
await bot.get_message_by_id(message_id: str) -> Message
```

Получает сообщение по ID.

## Методы: участники чата

### get_members

```python
await bot.get_members(
    chat_id: int,
    user_ids: list[int] | None = None,
    marker: int | None = None,
    count: int | None = None,
) -> list[ChatMember]
```

### add_members

```python
await bot.add_members(chat_id: int, user_ids: list[int]) -> bool
```

### remove_member

```python
await bot.remove_member(
    chat_id: int,
    user_id: int,
    block: bool | None = None,
) -> bool
```

### get_my_membership

```python
await bot.get_my_membership(chat_id: int) -> ChatMember
```

### leave_chat

```python
await bot.leave_chat(chat_id: int) -> bool
```

## Методы: администраторы

### get_admins

```python
await bot.get_admins(
    chat_id: int,
    marker: int | None = None,
) -> list[ChatMember]
```

### assign_admins

```python
await bot.assign_admins(
    chat_id: int,
    admins: list[dict[str, Any]],
) -> bool
```

### remove_admin

```python
await bot.remove_admin(chat_id: int, user_id: int) -> bool
```

## Методы: закреплённые сообщения

### get_pinned_message

```python
await bot.get_pinned_message(chat_id: int) -> Message | None
```

### pin_message

```python
await bot.pin_message(
    chat_id: int,
    message_id: str,
    notify: bool | None = None,
) -> bool
```

### unpin_message

```python
await bot.unpin_message(chat_id: int) -> bool
```

## Методы: действия в чате

### send_action

```python
await bot.send_action(chat_id: int, action: str) -> bool
```

Отправляет индикатор действия (например, «печатает...»).

Доступные действия (`ChatAction`):

- `typing_on` — печатает
- `sending_photo` — отправляет фото
- `sending_video` — отправляет видео
- `sending_audio` — отправляет аудио
- `sending_file` — отправляет файл
- `mark_seen` — прочитано

## Методы: callback

### answer_callback

```python
await bot.answer_callback(
    callback_id: str,
    text: str | None = None,
    attachments: list[Any] | None = None,
    notification: str | None = None,
    notify: bool | None = None,
    format: str | None = None,
) -> bool
```

Отвечает на callback-запрос от нажатия inline-кнопки.

- **callback_id** — ID callback-запроса
- **text** — текст ответного сообщения
- **notification** — текст уведомления (всплывающее)
- **attachments** — вложения к ответу

## Методы: подписки (webhooks)

### get_subscriptions

```python
await bot.get_subscriptions() -> list[Subscription]
```

### create_subscription

```python
await bot.create_subscription(
    url: str,
    update_types: list[str] | None = None,
    secret: str | None = None,
) -> bool
```

### delete_subscription

```python
await bot.delete_subscription(url: str) -> bool
```

## Методы: обновления

### get_updates

```python
await bot.get_updates(
    limit: int | None = None,
    timeout: int | None = None,
    marker: int | None = None,
    types: list[str] | None = None,
) -> list[Update]
```

Получает обновления через long polling.

!!! note

    Обычно вы не вызываете `get_updates()` напрямую — это делает `Dispatcher`.

## Методы: загрузка файлов

### get_upload_url

```python
await bot.get_upload_url(type: str) -> UploadInfo
```

Получает URL для загрузки файла. Типы: `"image"`, `"video"`, `"audio"`, `"file"`.

### upload_file

```python
await bot.upload_file(
    file_type: str,
    file_data: bytes,
    filename: str = "file",
) -> str
```

Двухэтапная загрузка файла. Возвращает токен для использования в вложениях.

## Методы: видео

### get_video_info

```python
await bot.get_video_info(video_token: str) -> VideoInfo
```

## Контекстный менеджер

Bot поддерживает `async with` для автоматического закрытия сессии:

```python
async with Bot(token="TOKEN") as bot:
    me = await bot.get_me()
    print(me.first_name)
# Сессия автоматически закрыта
```

## Выполнение произвольных методов

Bot можно вызывать как функцию, передавая объект `MaxMethod`:

```python
from maxgram.methods import SendMessage

result = await bot(SendMessage(
    chat_id=12345,
    text="Hello!",
))
```

## DefaultBotProperties

```python
from maxgram.client.default import DefaultBotProperties
from maxgram.enums import ParseMode

DefaultBotProperties(
    parse_mode: str | None = None,        # ParseMode.HTML или ParseMode.MARKDOWN
    disable_link_preview: bool | None = None,
    notify: bool | None = None,
)
```

Эти значения используются как значения по умолчанию при отправке сообщений,
если соответствующие параметры не указаны явно.
