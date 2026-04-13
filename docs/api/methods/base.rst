================
MaxMethod base
================

.. module:: maxgram.methods.base

Базовый класс для всех API-методов.

MaxMethod[T]
------------

.. code-block:: python

   class MaxMethod(BotContextController, BaseModel, Generic[MaxType], ABC):
       __returning__: ClassVar[type]   # Тип возвращаемого значения
       __http_method__: ClassVar[str]  # HTTP метод (GET, POST, PUT, PATCH, DELETE)
       __api_path__: ClassVar[str]     # Путь API (/messages, /chats/{chat_id})

       model_config = ConfigDict(
           extra="allow",
           populate_by_name=True,
           arbitrary_types_allowed=True,
       )

Методы
^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Метод
     - Описание
   * - ``build_request_path() -> str``
     - Подставляет параметры в ``__api_path__`` (например, ``{chat_id}`` → ``123``)
   * - ``build_query_params() -> dict``
     - Формирует query-параметры для GET/DELETE запросов
   * - ``build_request_body() -> dict | None``
     - Формирует JSON-тело для POST/PUT/PATCH запросов
   * - ``emit(bot) -> T``
     - Выполняет метод через переданный бот
   * - ``__await__() -> T``
     - Позволяет ``await method`` (требует привязанный bot через контекст)

Принцип работы
^^^^^^^^^^^^^^

1. ``build_request_path()`` формирует URL-путь
2. ``build_query_params()`` или ``build_request_body()`` формирует данные
3. Сессия выполняет HTTP-запрос
4. ``BaseSession.check_response()`` парсит ответ в ``__returning__`` тип

Response[T]
-----------

.. code-block:: python

   class Response(BaseModel, Generic[MaxType]):
       success: bool = True
       message: str | None = None
       result: MaxType | None = None

Обёртка ответа API. Используется для парсинга ответов вида ``{"success": true, "result": ...}``.

Пример создания метода
-----------------------

.. code-block:: python

   from maxgram.methods.base import MaxMethod
   from typing import ClassVar

   class MyCustomMethod(MaxMethod[bool]):
       __returning__: ClassVar[type] = bool
       __http_method__: ClassVar[str] = "POST"
       __api_path__: ClassVar[str] = "/custom/{entity_id}"

       entity_id: int
       value: str

   # Использование
   result = await bot(MyCustomMethod(entity_id=1, value="test"))

Исходный файл
--------------

``maxgram/methods/base.py``
