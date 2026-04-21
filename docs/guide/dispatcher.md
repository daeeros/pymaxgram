# Dispatcher и Router

Dispatcher и Router — основа системы маршрутизации событий в pymaxgram.

## Router

`Router` — маршрутизатор событий. Позволяет регистрировать
обработчики для различных типов событий.

### Создание

```python
from maxgram import Router

router = Router(name="my_router")  # name опционален
```

### Наблюдатели событий (observers)

Каждый роутер содержит наблюдатели для всех типов событий MAX API:

**Сообщения:**

| Декоратор | `update_type` | Описание |
| --- | --- | --- |
| `@router.message()` | `message_created` | Новое сообщение. Event: `Message` |
| `@router.message_callback()` | `message_callback` | Нажатие inline-кнопки. Event: `Callback` |
| `@router.message_edited()` | `message_edited` | Сообщение отредактировано. Event: `Message` |
| `@router.message_removed()` | `message_removed` | Сообщение удалено. Event: `Update` |

**Бот:**

| Декоратор | `update_type` | Описание |
| --- | --- | --- |
| `@router.bot_started()` | `bot_started` | Пользователь запустил бота. Event: `Update` |
| `@router.bot_stopped()` | `bot_stopped` | Пользователь остановил бота. Event: `Update` |
| `@router.bot_added()` | `bot_added` | Бот добавлен в чат. Event: `Update` |
| `@router.bot_removed()` | `bot_removed` | Бот удалён из чата. Event: `Update` |

**Пользователи и чат:**

| Декоратор | `update_type` | Описание |
| --- | --- | --- |
| `@router.user_added()` | `user_added` | Пользователь добавлен в чат. Event: `Update` |
| `@router.user_removed()` | `user_removed` | Пользователь удалён из чата. Event: `Update` |
| `@router.chat_title_changed()` | `chat_title_changed` | Изменено название чата. Event: `Update` |

**Диалоги:**

| Декоратор | `update_type` | Описание |
| --- | --- | --- |
| `@router.dialog_muted()` | `dialog_muted` | Уведомления отключены. Event: `Update` |
| `@router.dialog_unmuted()` | `dialog_unmuted` | Уведомления включены. Event: `Update` |
| `@router.dialog_cleared()` | `dialog_cleared` | Диалог очищен. Event: `Update` |
| `@router.dialog_removed()` | `dialog_removed` | Диалог удалён. Event: `Update` |

**Ошибки и жизненный цикл:**

- `@router.error()` — ошибки обработки
- `@router.startup()` — событие запуска
- `@router.shutdown()` — событие остановки

### Регистрация обработчиков

Через декораторы. Каждый тип события имеет свой типизированный класс:

```python
from maxgram.types import (
    Message, Callback,
    BotStarted, BotStopped, BotAdded, BotRemoved,
    UserAdded, UserRemoved, ChatTitleChanged,
    MessageRemoved, DialogMuted,
)

# Сообщения — event: Message
@router.message()
async def handle_message(message: Message, bot):
    await message.answer(text="Got it!")

@router.message_callback()
async def handle_callback(callback: Callback, bot):
    await callback.answer(notification="Clicked!")

@router.message_edited()
async def handle_edit(message: Message, bot):
    print(f"Message edited: {message.body.mid}")

# Бот — event: BotStarted, BotStopped, BotAdded, BotRemoved
@router.bot_started()
async def handle_start(event: BotStarted, bot):
    print(f"{event.user.first_name} started the bot")
    if event.payload:
        print(f"Raw payload: {event.payload}")
        print(f"Decoded: {event.deep_link()}")  # base64url decode

@router.bot_added()
async def handle_bot_added(event: BotAdded, bot):
    print(f"Bot added to chat {event.chat_id}, channel={event.is_channel}")

# Пользователи — event: UserAdded, UserRemoved
@router.user_added()
async def handle_user_added(event: UserAdded, bot):
    print(f"{event.user.first_name} joined chat {event.chat_id}")
    if event.inviter_id:
        print(f"Invited by {event.inviter_id}")

# Удаление сообщений — event: MessageRemoved
@router.message_removed()
async def handle_removed(event: MessageRemoved, bot):
    print(f"Message {event.message_id} removed from {event.chat_id}")

# Чат — event: ChatTitleChanged
@router.chat_title_changed()
async def handle_title(event: ChatTitleChanged, bot):
    print(f"New title: {event.title}")

# Диалоги — event: DialogMuted и т.д.
@router.dialog_muted()
async def handle_muted(event: DialogMuted, bot):
    print(f"Muted until {event.muted_until}")

@router.error()
async def handle_error(error, bot):
    pass

@router.startup()
async def on_startup(bot, dispatcher):
    print("Bot started!")

@router.shutdown()
async def on_shutdown(bot, dispatcher):
    print("Bot stopped!")
```

С фильтрами:

```python
from maxgram.filters import Command, StateFilter
from maxgram import F

@router.message(Command("help"))
async def help_cmd(message, bot):
    pass

@router.message(F.body.text == "hello")
async def hello(message, bot):
    pass

@router.message_callback(F.payload.startswith("action:"))
async def action(callback, bot):
    pass
```

### Вложенные роутеры

Роутеры можно вкладывать друг в друга для модульной архитектуры:

```python
from maxgram import Router

main_router = Router(name="main")
admin_router = Router(name="admin")
user_router = Router(name="user")

# Подключение одного роутера
main_router.include_router(admin_router)

# Подключение нескольких
main_router.include_routers(admin_router, user_router)
```

!!! important

    - Роутер может быть подключён только к одному родителю
    - Циклические ссылки запрещены
    - Событие проходит по дереву сверху вниз: сначала проверяются обработчики
      текущего роутера, затем дочерних

### Порядок обработки событий

1. Проверяются root-фильтры наблюдателя
2. Проверяются обработчики текущего роутера (в порядке регистрации)
3. Если ни один обработчик не сработал — событие передаётся дочерним роутерам
4. Первый совпавший обработчик обрабатывает событие

## Dispatcher

`Dispatcher` — корневой роутер, управляющий циклом получения
обновлений и их распределением.

### Создание

```python
from maxgram import Dispatcher
from maxgram.fsm.storage.memory import MemoryStorage
from maxgram.fsm.strategy import FSMStrategy

# Минимальный
dp = Dispatcher()

# С настройками FSM
dp = Dispatcher(
    storage=MemoryStorage(),
    fsm_strategy=FSMStrategy.USER_IN_CHAT,
    disable_fsm=False,
    name="main",
)
```

### Параметры конструктора

| Параметр | Тип | Описание |
| --- | --- | --- |
| `storage` | `BaseStorage \| None` | Хранилище FSM. По умолчанию `MemoryStorage()` |
| `fsm_strategy` | `FSMStrategy` | Стратегия FSM. По умолчанию `USER_IN_CHAT` |
| `events_isolation` | `BaseEventIsolation \| None` | Изоляция событий для конкурентности |
| `disable_fsm` | `bool` | Отключить FSM middleware (`False`) |
| `updates_debug` | `bool` | Логировать все входящие update в читаемом виде (`False`) |
| `requests_debug` | `bool` | Логировать все исходящие API-запросы (`False`) |
| `name` | `str \| None` | Имя диспетчера |
| `**kwargs` | `Any` | Данные workflow (доступны в обработчиках) |

### Встроенные middleware

Dispatcher автоматически регистрирует три outer middleware на наблюдателе `update`:

1. **ErrorsMiddleware** — перехватывает исключения и направляет их в обработчики ошибок
2. **UserContextMiddleware** — извлекает контекст пользователя/чата из обновления
3. **FSMContextMiddleware** — предоставляет FSM-контекст в обработчики

### Long Polling

```python
import asyncio
from maxgram import Bot, Dispatcher

bot = Bot(token="TOKEN")
dp = Dispatcher()

# Вариант 1: async
asyncio.run(dp.start_polling(bot))

# Вариант 2: блокирующий (с поддержкой uvloop)
dp.run_polling(bot)
```

Параметры `start_polling()`:

| Параметр | Тип | Описание |
| --- | --- | --- |
| `*bots` | `Bot` | Один или несколько экземпляров Bot |
| `polling_timeout` | `int` | Серверный long-polling hint: сколько MAX держит соединение, ожидая апдейты (по умолчанию 10 сек) |
| `request_timeout` | `float \| None` | Клиентский жёсткий таймаут на один `GET /updates` HTTP-запрос. `None` (дефолт) = `polling_timeout + 5`. Срезает зависшие соединения, чтобы backoff/retry срабатывал быстро |
| `drop_pending_updates` | `bool` | Перед стартом выполнить один `GetUpdates(timeout=0)`, отбросить его результат и продолжить с нового маркера. Полезно после рестарта, чтобы не обрабатывать накопившуюся очередь (`False` по умолчанию) |
| `handle_as_tasks` | `bool` | Обрабатывать обновления в отдельных задачах (`True`) |
| `backoff_config` | `BackoffConfig` | Настройки экспоненциального отступления при ошибках |
| `allowed_updates` | `list[str] \| None` | Список типов обновлений. По умолчанию — автоопределение |
| `handle_signals` | `bool` | Обрабатывать SIGINT/SIGTERM (`True`) |
| `close_bot_session` | `bool` | Закрывать сессию бота при остановке (`True`) |
| `tasks_concurrency_limit` | `int \| None` | Лимит параллельных задач обработки |

#### Два таймаута: `polling_timeout` vs `request_timeout`

Это **разные** вещи, и их часто путают:

- **`polling_timeout`** — hint серверу MAX: «держи соединение открытым до N секунд, ожидая новых апдейтов». Отправляется как query-параметр `?timeout=N`. Сам сервер решает, когда отпустить запрос.
- **`request_timeout`** — клиентский жёсткий лимит aiohttp: «я жду этот HTTP-запрос максимум N секунд, после чего рву». Если MAX иногда держит соединение дольше, чем обещал, или вообще залипает, этот таймаут отрубит его и backoff-цикл перезапустится.

Дефолт `request_timeout = polling_timeout + 5` — минимальный запас на handshake + ответ. Если у тебя сеть с высокой задержкой или MAX ведёт себя непредсказуемо, можно задать явно:

```python
# Агрессивно: если MAX не ответил за 8с — отрубить, подождать 1с, попробовать снова
dp.run_polling(bot, polling_timeout=5, request_timeout=8)

# Более щадящий режим для нестабильной сети
dp.run_polling(bot, polling_timeout=25, request_timeout=40)
```

#### Сброс очереди при запуске

Если бот перезапускается и **не должен обрабатывать старые события**, накопившиеся в очереди MAX:

```python
dp.run_polling(bot, drop_pending_updates=True)
```

Перед входом в цикл один раз вызывается `GetUpdates(timeout=0)`, пришедшие апдейты отбрасываются, маркер сдвигается на текущий head. В логе будет:

```
Dropped 12 pending update(s), resuming from marker=777 for bot id=267960700
```

Если сам drain упадёт (сеть, 5xx) — это не фатально: пишем `WARNING` и продолжаем polling с нулевым маркером.

### Workflow Data

Dispatcher поддерживает хранение данных, доступных во всех обработчиках:

```python
dp = Dispatcher()

# Через конструктор
dp = Dispatcher(db=database, config=settings)

# Через dict-интерфейс
dp["db"] = database
dp["config"] = settings

# Доступ в обработчике
@router.message()
async def handler(message, bot, db, config):
    # db и config автоматически инъектируются
    pass
```

### Webhook-режим

```python
await dp.feed_webhook_update(bot, update)
await dp.feed_raw_update(bot, raw_dict)
```

### Остановка

```python
await dp.stop_polling()
```

### Многоботовый режим

```python
bot1 = Bot(token="TOKEN_1")
bot2 = Bot(token="TOKEN_2")

dp = Dispatcher()
# Оба бота используют одни и те же обработчики
await dp.start_polling(bot1, bot2)
```

### Режим отладки

```python
dp = Dispatcher(
    updates_debug=True,     # Логировать входящие update
    requests_debug=True,    # Логировать исходящие API-запросы
)
```

`updates_debug=True` выводит для каждого update:

```text
============================================================
UPDATE message_callback
  from: Michael (id=248173258)
  payload: 'adm:plg:'
  callback_id: f9LHodD0cOKe8x...
  message_mid: mid.ffffbd399a199736
============================================================
  -> HANDLED in 15 ms (type=message_callback)
```

`requests_debug=True` выводит для каждого API-вызова:

```text
POST /answers params={'callback_id': 'abc'} body={'message': {'text': '...'}}
  -> bool
```
