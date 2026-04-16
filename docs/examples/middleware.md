# Middleware

Примеры пользовательских middleware.

## Логирование

```python
import time
import logging
from typing import Any
from collections.abc import Awaitable, Callable
from maxgram import BaseMiddleware
from maxgram.types import MaxObject

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[MaxObject, dict[str, Any]], Awaitable[Any]],
        event: MaxObject,
        data: dict[str, Any],
    ) -> Any:
        start = time.monotonic()
        result = await handler(event, data)
        duration = time.monotonic() - start
        logger.info("Handler completed in %.3fs", duration)
        return result

# Регистрация
router.message.outer_middleware(LoggingMiddleware())
```

## Авторизация

```python
class AuthMiddleware(BaseMiddleware):
    def __init__(self, allowed_user_ids: set[int]):
        self.allowed_user_ids = allowed_user_ids

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        if user and user.user_id not in self.allowed_user_ids:
            return  # Игнорируем неавторизованных
        return await handler(event, data)

router.message.outer_middleware(
    AuthMiddleware(allowed_user_ids={123456, 789012})
)
```

## Инъекция данных

```python
class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def __call__(self, handler, event, data):
        async with self.db_pool.acquire() as conn:
            data["db"] = conn
            return await handler(event, data)

# В обработчике
@router.message()
async def handler(message, bot, db):
    result = await db.fetch("SELECT * FROM users")
```
