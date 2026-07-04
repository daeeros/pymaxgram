# Session

HTTP-сессии для выполнения запросов к MAX API.

## BaseSession

Абстрактный базовый класс для всех сессий.

```python
class BaseSession(ABC):
    api: MaxAPIServer = PRODUCTION
    json_loads: Callable = json.loads
    json_dumps: Callable = json.dumps
    timeout: float | int | None = None
    middleware: RequestMiddlewareManager
```

### Методы

| Метод | Описание |
| --- | --- |
| `check_response(bot, method, status_code, content)` | Парсит ответ API и маппит HTTP-коды на исключения |
| `make_request(bot, method, timeout?)` | Абстрактный. Выполняет HTTP-запрос |
| `stream_content(url, headers?, timeout?, chunk_size?)` | Абстрактный. Потоковое чтение контента |
| `close()` | Абстрактный. Закрывает сессию |
| `__call__(bot, method, **kwargs)` | Вызывает `make_request` через middleware-цепочку |

### Маппинг HTTP-кодов на исключения

| Код | Исключение | Описание |
| --- | --- | --- |
| 400 | `MaxBadRequest` | Некорректный запрос |
| 401 | `MaxUnauthorizedError` | Недействительный токен |
| 403 | `MaxForbiddenError` | Доступ запрещён |
| 404 | `MaxNotFound` | Ресурс не найден |
| 409 | `MaxConflictError` | Конфликт |
| 429 | `MaxRateLimitError` | Превышен лимит |
| 503 | `MaxServiceUnavailable` | Сервис недоступен |
| 5xx | `MaxServerError` | Ошибка сервера |

## AiohttpSession

Реализация на базе aiohttp.

```python
from maxgram.client.session.aiohttp import AiohttpSession

session = AiohttpSession(
    proxy: str | None = None,       # Прокси (HTTP/SOCKS)
    timeout: float | int = 300,     # Таймаут запросов
)
```

Возможности:

- **Прокси** — поддержка HTTP и SOCKS через `aiohttp-socks`
- **SSL** — автоматическое использование `certifi` для TLS
- **DNS-кэширование** — 10-секундный TTL
- **Лимит соединений** — 100 одновременных
- **User-Agent** — `pymaxgram/4.0.1`
- **Загрузка файлов** — через `upload_file(bot, upload_url, file_data, filename)`

## Request Middleware

Middleware для перехвата HTTP-запросов.

### RequestMiddlewareManager

Управляет цепочкой request middleware:

```python
session.middleware.register(MyRequestMiddleware())
```

### BaseRequestMiddleware

```python
class BaseRequestMiddleware(ABC):
    async def __call__(self, make_request, bot, method, **kwargs):
        return await make_request(bot, method, **kwargs)
```

### RequestLogging

Встроенный middleware для логирования запросов.

## MaxAPIServer

```python
from maxgram.client.max_api import MaxAPIServer, PRODUCTION

MaxAPIServer(base="https://platform-api2.max.ru")

# Методы
server.api_url("/me")  # "https://platform-api2.max.ru/me"
MaxAPIServer.from_base("https://custom-api.example.com")

# Константа
PRODUCTION = MaxAPIServer(base="https://platform-api2.max.ru")
```

## Сертификат Минцифры (TLS)

Хост `platform-api2.max.ru` использует TLS-сертификат, выпущенный удостоверяющим центром
Минцифры России (*Russian Trusted Root CA*), которого нет в стандартном наборе `certifi`.
pymaxgram поставляет этот сертификат в комплекте и доверяет ему **по умолчанию**, поэтому
запросы работают из коробки.

```python
from maxgram.client.session.aiohttp import AiohttpSession

# По умолчанию сертификат Минцифры доверенный
session = AiohttpSession()

# Отключить доверие к CA Минцифры
session = AiohttpSession(trust_russian_ca=False)

# Полностью свой SSL-контекст (переопределяет trust_russian_ca)
import ssl
session = AiohttpSession(ssl_context=ssl.create_default_context())
```

## Исходные файлы

- `maxgram/client/session/base.py`
- `maxgram/client/session/aiohttp.py`
- `maxgram/client/session/middlewares/`
- `maxgram/client/max_api.py`
