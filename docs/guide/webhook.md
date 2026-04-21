# Webhook-режим

Помимо long polling, pymaxgram поддерживает получение обновлений через webhook. Высокоуровневый API позволяет поднять полноценный production-ready сервер одной строкой — фреймворк сам поднимает HTTP-сервер, регистрирует подписку в MAX, обрабатывает сигналы и удаляет подписку при остановке.

## Быстрый старт

```python
from maxgram import Bot, Dispatcher

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()

@dp.message()
async def echo(message):
    await message.answer(message.body.text)

dp.run_webhook(
    bot,
    url="https://max.example.com/webhook",  # публичный HTTPS-URL
    secret="your_secret",                    # X-Max-Bot-Api-Secret
    host="127.0.0.1",                        # локальный bind (за reverse-proxy)
    port=8080,
)
```

`url` — это публичный адрес, который регистрируется в MAX (туда летят POST-запросы от MAX). `host`/`port` — локальный bind aiohttp. Путь (`/webhook`) автоматически берётся из `url`. По Ctrl+C сервер корректно останавливается, и подписка снимается.

## Сценарии разворачивания

### За reverse-proxy (рекомендуется)

Внешний HTTPS терминирует ваш reverse-proxy (nginx, caddy, traefik), который проксирует запросы на локальный `http://127.0.0.1:8080`. Pymaxgram слушает HTTP — SSL-параметры не нужны:

```python
dp.run_webhook(
    bot,
    url="https://max.example.com/webhook",
    secret="...",
    host="127.0.0.1",
    port=8080,
)
```

### Прямой HTTPS без прокси

Pymaxgram сам терминирует TLS:

```python
dp.run_webhook(
    bot,
    url="https://max.example.com/webhook",
    secret="...",
    host="0.0.0.0",
    port=443,
    ssl_certfile="/etc/letsencrypt/live/max.example.com/fullchain.pem",
    ssl_keyfile="/etc/letsencrypt/live/max.example.com/privkey.pem",
)
```

## Параметры `run_webhook` / `start_webhook`

| Параметр | По умолчанию | Описание |
| --- | --- | --- |
| `url` | — (обязательный) | Публичный URL, регистрируется как подписка в MAX |
| `secret` | `None` | Токен заголовка `X-Max-Bot-Api-Secret` |
| `host` | `"0.0.0.0"` | Локальный bind |
| `port` | `8080` | Локальный порт |
| `path` | из `url` | Путь HTTP-роута |
| `allowed_updates` | `UNSET` (авто) | Типы апдейтов; `UNSET` → автоматически из зарегистрированных хэндлеров |
| `drop_pending_updates` | `False` | Удалить старую подписку перед созданием новой |
| `register_subscription` | `True` | Автоматически создавать/удалять подписку при старте/остановке |
| `handle_in_background` | `True` | Обрабатывать апдейты в фоновых тасках, отвечая 200 моментально |
| `ssl_certfile` / `ssl_keyfile` | `None` | PEM-файлы для прямого HTTPS |
| `ssl_context` | `None` | Готовый `ssl.SSLContext` |
| `ip_filter` | `None` | `IPFilter` или список IP/CIDR для фильтрации |
| `handle_signals` | `True` | Обработка `SIGINT`/`SIGTERM` |
| `close_bot_session` | `True` | Закрыть `bot.session` после остановки |
| `access_log` | `False` | `True` — включить access-лог через `maxgram.loggers.webhook` |
| `app` | `None` | Существующий `aiohttp.web.Application` для встраивания |

## Async-вариант

`start_webhook` — корутина для встраивания в собственный event loop:

```python
import asyncio

async def main():
    await dp.start_webhook(
        bot,
        url="https://max.example.com/webhook",
        secret="...",
    )

asyncio.run(main())
```

## Производительность

`run_webhook` автоматически использует `uvloop` (Linux/macOS), если он установлен — тот же механизм, что и в `run_polling`. Если установлен `orjson`, он автоматически подменяет `json.loads`/`dumps` на время работы webhook-сессии.

Установите оба ускорителя одной командой:

```bash
pip install pymaxgram[fast]
```

## IP-фильтрация

```python
dp.run_webhook(
    bot,
    url="https://max.example.com/webhook",
    secret="...",
    ip_filter=["1.2.3.4", "10.0.0.0/24"],
)
```

Фильтр корректно работает за reverse-proxy — учитывается заголовок `X-Forwarded-For`.

## Продвинутое использование

Если нужен полный контроль — например, встроить webhook в существующее aiohttp-приложение со своими роутами, — используйте низкоуровневые компоненты:

```python
from aiohttp import web
from maxgram.webhook import SimpleRequestHandler, setup_application

app = web.Application()
handler = SimpleRequestHandler(dp, bot, secret_token="your_secret")
handler.register(app, "/webhook")
setup_application(app, dp)
web.run_app(app, host="0.0.0.0", port=8080)
```

В этом случае подписку нужно регистрировать самостоятельно:

```python
@dp.startup()
async def on_startup(bot, dispatcher):
    await bot.create_subscription(
        url="https://max.example.com/webhook",
        update_types=["message_created", "message_callback", "bot_started"],
        secret="your_secret",
    )

@dp.shutdown()
async def on_shutdown(bot, dispatcher):
    await bot.delete_subscription(url="https://max.example.com/webhook")
```

### Кастомный обработчик

Для мульти-бот режима — наследник `BaseRequestHandler`:

```python
from maxgram.webhook import BaseRequestHandler

class MyHandler(BaseRequestHandler):
    async def resolve_bot(self, request) -> Bot:
        # Логика определения бота из request
        ...

    def verify_secret(self, secret_token: str, bot: Bot) -> bool:
        ...

    async def close(self) -> None:
        ...
```

## Polling vs Webhook

|  | Polling | Webhook |
| --- | --- | --- |
| **Простота** | Проще настроить | Нужен публичный домен + TLS |
| **Задержка** | Зависит от timeout | Мгновенная доставка |
| **Нагрузка** | Постоянные запросы к API | Запросы только при событиях |
| **Для разработки** | Подходит | Нужен публичный URL (ngrok/cloudflared) |
| **Для продакшена** | Для малых нагрузок | Рекомендуется |
