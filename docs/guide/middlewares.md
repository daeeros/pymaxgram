# Middleware

Middleware позволяют перехватывать и модифицировать процесс обработки событий.

## Принцип работы

Middleware оборачивают обработчик, образуя цепочку:

```text
Middleware 1 → Middleware 2 → ... → Handler
```

Каждый middleware может:

- Выполнить код **до** обработчика
- Выполнить код **после** обработчика
- Модифицировать данные
- Прервать обработку (не вызывая `handler`)

## Создание middleware

```python
from typing import Any
from collections.abc import Awaitable, Callable
from maxgram import BaseMiddleware
from maxgram.types import MaxObject

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[MaxObject, dict[str, Any]], Awaitable[Any]],
        event: MaxObject,
        data: dict[str, Any],
    ) -> Any:
        print(f"Before: {event}")
        result = await handler(event, data)
        print(f"After: {result}")
        return result
```

Параметры `__call__`:

- **handler** — следующий обработчик (или middleware) в цепочке
- **event** — объект события (Message, Callback, Update)
- **data** — словарь данных (bot, state, event_from_user и т.д.)

## Регистрация

Два уровня middleware:

### Outer middleware

Выполняется для **всех** событий данного типа, независимо от наличия обработчика:

```python
# На конкретный тип событий
router.message.outer_middleware(LoggingMiddleware())
router.message_callback.outer_middleware(AuthMiddleware())

# На уровне Dispatcher (update) — для всех событий
dp.update.outer_middleware(GlobalMiddleware())
```

### Inner middleware

Выполняется только если найден подходящий обработчик:

```python
router.message.middleware(LoggingMiddleware())
```

## Примеры

### Middleware авторизации

```python
class AuthMiddleware(BaseMiddleware):
    def __init__(self, allowed_ids: set[int]):
        self.allowed_ids = allowed_ids

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        if user and user.user_id not in self.allowed_ids:
            return  # Прерываем обработку
        return await handler(event, data)

router.message.outer_middleware(AuthMiddleware({123456, 789012}))
```

### Middleware замера времени

```python
import time

class TimingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        start = time.monotonic()
        result = await handler(event, data)
        duration = time.monotonic() - start
        print(f"Handler took {duration:.3f}s")
        return result
```

### Middleware инъекции данных

```python
class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db):
        self.db = db

    async def __call__(self, handler, event, data):
        data["db"] = self.db
        return await handler(event, data)

# В обработчике
@router.message()
async def handler(message, bot, db):
    # db доступен из middleware
    pass
```

### Middleware троттлинга

```python
import time

class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, rate: float = 1.0):
        self.rate = rate
        self.last_call: dict[int, float] = {}

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        if user:
            now = time.monotonic()
            last = self.last_call.get(user.user_id, 0)
            if now - last < self.rate:
                return  # Слишком частые запросы
            self.last_call[user.user_id] = now
        return await handler(event, data)
```

## Встроенные middleware

Dispatcher автоматически регистрирует:

| Middleware | Описание |
| --- | --- |
| `ErrorsMiddleware` | Перехватывает исключения, направляет в `router.error` |
| `UserContextMiddleware` | Извлекает `event_from_user`, `event_chat`, `event_context` из Update |
| `FSMContextMiddleware` | Предоставляет `state` (FSMContext) и `raw_state` в данные обработчика |

## Данные, доступные в обработчиках

После прохождения встроенных middleware, в `data` доступны:

| Ключ | Тип | Описание |
| --- | --- | --- |
| `bot` | `Bot` | Экземпляр бота |
| `event_update` | `Update` | Исходное обновление |
| `event_router` | `Router` | Роутер, обработавший событие |
| `event_from_user` | `User \| None` | Отправитель |
| `event_chat` | `int \| None` | ID чата |
| `event_context` | `EventContext` | Контекст события |
| `state` | `FSMContext` | FSM-контекст |
| `raw_state` | `str \| None` | Строковое значение состояния |
| `fsm_storage` | `BaseStorage` | Хранилище FSM |
| `dispatcher` | `Dispatcher` | Диспетчер |
