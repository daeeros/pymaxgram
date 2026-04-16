# pymaxgram --- документация

[![PyPI version](https://img.shields.io/pypi/v/pymaxgram.svg)](https://pypi.org/project/pymaxgram/)
[![Python versions](https://img.shields.io/pypi/pyversions/pymaxgram.svg)](https://pypi.org/project/pymaxgram/)
[![License](https://img.shields.io/github/license/daeeros/pymaxgram.svg)](https://github.com/daeeros/pymaxgram/blob/main/LICENSE)

**pymaxgram** --- асинхронный Python-фреймворк для создания ботов на платформе [MAX Messenger](https://max.ru).

Построен на базе `asyncio`, `aiohttp` и `pydantic`. Вдохновлён архитектурой [aiogram](https://aiogram.dev).

## Быстрый старт

```python
import asyncio
from maxgram import Bot, Dispatcher, Router

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()
router = Router()

@router.message()
async def echo(message, bot):
    await message.answer(text=message.body.text)

dp.include_router(router)
asyncio.run(dp.start_polling(bot))
```

## Возможности

- Полностью асинхронный (asyncio + aiohttp)
- Типизация данных через Pydantic v2
- Система фильтров (команды, callback data, FSM-состояния, magic filter)
- Конечные автоматы (FSM) с поддержкой стратегий
- Middleware на уровне запросов и событий
- Inline-клавиатуры и обработка callback
- Форматирование текста (HTML / Markdown)
- Загрузка файлов (из памяти, файловой системы, URL)
- Webhook-режим через aiohttp
- Модульная архитектура с вложенными роутерами
