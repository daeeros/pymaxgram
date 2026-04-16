# Webhook

## setup_application

```python
def setup_application(
    app: web.Application,
    dispatcher: Dispatcher,
    **kwargs,
) -> None
```

Привязывает Dispatcher к aiohttp Application:

- `on_startup` → `dispatcher.emit_startup()`
- `on_shutdown` → `dispatcher.emit_shutdown()`

## BaseRequestHandler

```python
class BaseRequestHandler(ABC):
    def __init__(self, dispatcher, **kwargs) -> None: ...

    def register(self, app, path) -> None
    async def handle(self, request) -> web.Response
    async def resolve_bot(self, request) -> Bot  # Абстрактный
```

## SimpleRequestHandler

```python
class SimpleRequestHandler(BaseRequestHandler):
    def __init__(
        self,
        dispatcher: Dispatcher,
        bot: Bot,
        secret_token: str | None = None,
        **kwargs,
    ) -> None: ...
```

- Для одного бота
- Проверяет `X-Max-Bot-Api-Secret` заголовок
- Парсит JSON-тело → `Update` → `dispatcher.feed_webhook_update()`

## IPFilter

```python
class IPFilter:
    def __init__(self, ips: list[str | IPv4Address | IPv4Network]) -> None: ...

    def check(self, ip: str) -> bool
```

## ip_filter_middleware

```python
def ip_filter_middleware(ip_filter: IPFilter) -> web.middleware
```

Aiohttp middleware для фильтрации IP-адресов.

## Пример

```python
from aiohttp import web
from maxgram import Bot, Dispatcher
from maxgram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

bot = Bot(token="TOKEN")
dp = Dispatcher()

app = web.Application()
handler = SimpleRequestHandler(dp, bot, secret_token="secret")
handler.register(app, "/webhook")
setup_application(app, dp)
web.run_app(app, host="0.0.0.0", port=8080)
```

## Исходные файлы

- `maxgram/webhook/aiohttp_server.py`
- `maxgram/webhook/security.py`
