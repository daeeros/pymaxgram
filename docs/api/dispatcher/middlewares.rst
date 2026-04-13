=====================
Middleware диспетчера
=====================

.. module:: maxgram.dispatcher.middlewares

BaseMiddleware
--------------

.. code-block:: python

   class BaseMiddleware(ABC):
       async def __call__(
           self,
           handler: Callable[[MaxObject, dict[str, Any]], Awaitable[Any]],
           event: MaxObject,
           data: dict[str, Any],
       ) -> Any: ...

MiddlewareManager
-----------------

Управляет цепочкой middleware (inner или outer).

.. code-block:: python

   class MiddlewareManager(Sequence):
       def register(self, middleware) -> None
       def unregister(self, middleware) -> None
       async def wrap_middlewares(self, middlewares, handler, event, data) -> Any

ErrorsMiddleware
----------------

Перехватывает исключения из обработчиков и передаёт в ``router.error``.

.. code-block:: python

   class ErrorsMiddleware(BaseMiddleware):
       def __init__(self, router: Router) -> None

Поведение:

1. Вызывает ``handler(event, data)``
2. При исключении создаёт ``ErrorEvent(update=..., exception=...)``
3. Передаёт в ``router.propagate_event("error", error_event, ...)``
4. Если обработчик ошибок не найден — пробрасывает исключение

UserContextMiddleware
---------------------

Извлекает контекст пользователя/чата из Update.

.. code-block:: python

   class UserContextMiddleware(BaseMiddleware):
       ...

Добавляет в ``data``:

- ``event_context`` — ``EventContext(user, chat_id)``
- ``event_from_user`` — ``User | None``
- ``event_chat`` — ``int | None``

EventContext
^^^^^^^^^^^^

.. code-block:: python

   @dataclass
   class EventContext:
       user: User | None = None
       chat_id: int | None = None

       @property
       def user_id(self) -> int | None

FSMContextMiddleware
--------------------

Предоставляет FSM-контекст в обработчики.

.. code-block:: python

   class FSMContextMiddleware(BaseMiddleware):
       def __init__(
           self,
           storage: BaseStorage,
           strategy: FSMStrategy,
           events_isolation: BaseEventIsolation,
       ) -> None

Добавляет в ``data``:

- ``state`` — ``FSMContext``
- ``raw_state`` — ``str | None``
- ``fsm_storage`` — ``BaseStorage``

Исходные файлы
--------------

- ``maxgram/dispatcher/middlewares/base.py``
- ``maxgram/dispatcher/middlewares/manager.py``
- ``maxgram/dispatcher/middlewares/error.py``
- ``maxgram/dispatcher/middlewares/user_context.py``
- ``maxgram/fsm/middleware.py``
