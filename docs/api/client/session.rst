=========
Session
=========

.. module:: maxgram.client.session

HTTP-сессии для выполнения запросов к MAX API.

BaseSession
-----------

Абстрактный базовый класс для всех сессий.

.. code-block:: python

   class BaseSession(ABC):
       api: MaxAPIServer = PRODUCTION
       json_loads: Callable = json.loads
       json_dumps: Callable = json.dumps
       timeout: float | int | None = None
       middleware: RequestMiddlewareManager

Методы
^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Метод
     - Описание
   * - ``check_response(bot, method, status_code, content)``
     - Парсит ответ API и маппит HTTP-коды на исключения
   * - ``make_request(bot, method, timeout?)``
     - Абстрактный. Выполняет HTTP-запрос
   * - ``stream_content(url, headers?, timeout?, chunk_size?)``
     - Абстрактный. Потоковое чтение контента
   * - ``close()``
     - Абстрактный. Закрывает сессию
   * - ``__call__(bot, method, **kwargs)``
     - Вызывает ``make_request`` через middleware-цепочку

Маппинг HTTP-кодов на исключения
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Код
     - Исключение
     - Описание
   * - 400
     - ``MaxBadRequest``
     - Некорректный запрос
   * - 401
     - ``MaxUnauthorizedError``
     - Недействительный токен
   * - 403
     - ``MaxForbiddenError``
     - Доступ запрещён
   * - 404
     - ``MaxNotFound``
     - Ресурс не найден
   * - 409
     - ``MaxConflictError``
     - Конфликт
   * - 429
     - ``MaxRateLimitError``
     - Превышен лимит
   * - 503
     - ``MaxServiceUnavailable``
     - Сервис недоступен
   * - 5xx
     - ``MaxServerError``
     - Ошибка сервера

AiohttpSession
--------------

Реализация на базе aiohttp.

.. code-block:: python

   from maxgram.client.session.aiohttp import AiohttpSession

   session = AiohttpSession(
       proxy: str | None = None,       # Прокси (HTTP/SOCKS)
       timeout: float | int = 300,     # Таймаут запросов
   )

Возможности:

- **Прокси** — поддержка HTTP и SOCKS через ``aiohttp-socks``
- **SSL** — автоматическое использование ``certifi`` для TLS
- **DNS-кэширование** — 10-секундный TTL
- **Лимит соединений** — 100 одновременных
- **User-Agent** — ``pymaxgram/4.0.1``
- **Загрузка файлов** — через ``upload_file(bot, upload_url, file_data, filename)``

Request Middleware
------------------

Middleware для перехвата HTTP-запросов.

RequestMiddlewareManager
^^^^^^^^^^^^^^^^^^^^^^^^

Управляет цепочкой request middleware:

.. code-block:: python

   session.middleware.register(MyRequestMiddleware())

BaseRequestMiddleware
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class BaseRequestMiddleware(ABC):
       async def __call__(self, make_request, bot, method, **kwargs):
           return await make_request(bot, method, **kwargs)

RequestLogging
^^^^^^^^^^^^^^

Встроенный middleware для логирования запросов.

MaxAPIServer
------------

.. code-block:: python

   from maxgram.client.max_api import MaxAPIServer, PRODUCTION

   MaxAPIServer(base="https://platform-api.max.ru")

   # Методы
   server.api_url("/me")  # "https://platform-api.max.ru/me"
   MaxAPIServer.from_base("https://custom-api.example.com")

   # Константа
   PRODUCTION = MaxAPIServer(base="https://platform-api.max.ru")

Исходные файлы
--------------

- ``maxgram/client/session/base.py``
- ``maxgram/client/session/aiohttp.py``
- ``maxgram/client/session/middlewares/``
- ``maxgram/client/max_api.py``
