==================
Обработка ошибок
==================

pymaxgram предоставляет систему обработки ошибок на нескольких уровнях.

Обработчики ошибок
------------------

Регистрация через декоратор ``@router.error()``:

.. code-block:: python

   from maxgram import Router
   from maxgram.filters import ExceptionTypeFilter, ExceptionMessageFilter

   router = Router()

   # По типу исключения
   @router.error(ExceptionTypeFilter(ValueError))
   async def handle_value_error(error, bot):
       print(f"ValueError: {error}")

   # По тексту (regex)
   @router.error(ExceptionMessageFilter(r"timeout"))
   async def handle_timeout(error, bot):
       print("Timeout occurred")

   # Все ошибки (fallback)
   @router.error()
   async def handle_all(error, bot):
       print(f"Unhandled: {error}")

Иерархия исключений
--------------------

.. code-block:: text

   MaxgramError (базовое)
   ├── DetailedMaxgramError
   │   ├── MaxAPIError
   │   │   ├── MaxNetworkError
   │   │   ├── MaxBadRequest (400)
   │   │   ├── MaxUnauthorizedError (401)
   │   │   ├── MaxForbiddenError (403)
   │   │   ├── MaxNotFound (404)
   │   │   ├── MaxConflictError (409)
   │   │   ├── MaxRateLimitError (429)
   │   │   ├── MaxServerError (5xx)
   │   │   │   └── MaxServiceUnavailable (503)
   │   │   └── ClientDecodeError
   │   ├── DataNotDictLikeError
   │   └── UnsupportedKeywordArgument
   └── ClientDecodeError

Исключения API
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Исключение
     - HTTP код
     - Описание
   * - ``MaxBadRequest``
     - 400
     - Некорректный запрос
   * - ``MaxUnauthorizedError``
     - 401
     - Недействительный токен
   * - ``MaxForbiddenError``
     - 403
     - Доступ запрещён
   * - ``MaxNotFound``
     - 404
     - Ресурс не найден
   * - ``MaxConflictError``
     - 409
     - Конфликт (например, дублирование)
   * - ``MaxRateLimitError``
     - 429
     - Превышен лимит запросов
   * - ``MaxServerError``
     - 5xx
     - Ошибка сервера
   * - ``MaxServiceUnavailable``
     - 503
     - Сервис недоступен
   * - ``MaxNetworkError``
     - —
     - Ошибка сети (таймаут и т.д.)

Обработка API-ошибок
---------------------

.. code-block:: python

   from maxgram.exceptions import MaxBadRequest, MaxRateLimitError

   @router.error(ExceptionTypeFilter(MaxRateLimitError))
   async def handle_rate_limit(error, bot):
       print("Rate limit! Waiting...")

   @router.error(ExceptionTypeFilter(MaxBadRequest))
   async def handle_bad_request(error, bot):
       print(f"Bad request: {error}")

Try/except в обработчиках
--------------------------

.. code-block:: python

   from maxgram.exceptions import MaxAPIError

   @router.message()
   async def handler(message, bot):
       try:
           await bot.send_message(chat_id=12345, text="Hello")
       except MaxAPIError as e:
           print(f"API error: {e}")

Middleware ErrorsMiddleware
---------------------------

Встроенный middleware ``ErrorsMiddleware`` автоматически перехватывает все
исключения из обработчиков и перенаправляет их в наблюдатель ``error``.

Порядок:

1. Обработчик выбрасывает исключение
2. ``ErrorsMiddleware`` перехватывает его
3. Создаётся ``ErrorEvent`` с update и exception
4. Событие передаётся в ``router.error`` обработчики
5. Если ни один обработчик не поймал — исключение логируется
