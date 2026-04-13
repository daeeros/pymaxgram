========
Router
========

.. module:: maxgram.dispatcher.router

Маршрутизатор событий.

.. code-block:: python

   class Router:
       def __init__(self, *, name: str | None = None) -> None: ...

Атрибуты
--------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Атрибут
     - Тип
     - Описание
   * - ``name``
     - ``str``
     - Имя роутера (по умолчанию ``hex(id(self))``)
   * - ``message``
     - ``MaxEventObserver``
     - Наблюдатель событий ``message_created``
   * - ``message_callback``
     - ``MaxEventObserver``
     - Наблюдатель событий ``message_callback``
   * - ``bot_started``
     - ``MaxEventObserver``
     - Наблюдатель событий ``bot_started``
   * - ``error`` / ``errors``
     - ``MaxEventObserver``
     - Наблюдатель ошибок
   * - ``startup``
     - ``EventObserver``
     - Событие запуска
   * - ``shutdown``
     - ``EventObserver``
     - Событие остановки
   * - ``sub_routers``
     - ``list[Router]``
     - Дочерние роутеры
   * - ``observers``
     - ``dict[str, MaxEventObserver]``
     - Словарь наблюдателей по именам

Методы
------

include_router
^^^^^^^^^^^^^^

.. code-block:: python

   def include_router(self, router: Router) -> Router

Подключает дочерний роутер. Устанавливает ``parent_router``.

include_routers
^^^^^^^^^^^^^^^

.. code-block:: python

   def include_routers(self, *routers: Router) -> None

Подключает несколько дочерних роутеров.

propagate_event
^^^^^^^^^^^^^^^

.. code-block:: python

   async def propagate_event(
       self,
       update_type: str,
       event: MaxObject,
       **kwargs,
   ) -> Any

Передаёт событие по дереву роутеров. Возвращает результат обработчика или ``UNHANDLED``.

resolve_used_update_types
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def resolve_used_update_types(
       self,
       skip_events: set[str] | None = None,
   ) -> list[str]

Определяет типы обновлений, для которых зарегистрированы обработчики.

emit_startup / emit_shutdown
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   async def emit_startup(self, *args, **kwargs) -> None
   async def emit_shutdown(self, *args, **kwargs) -> None

Вызывает события жизненного цикла рекурсивно по дереву роутеров.

Свойства
--------

- ``parent_router`` → ``Router | None`` — родительский роутер
- ``chain_head`` → генератор от текущего к корню
- ``chain_tail`` → генератор от текущего ко всем потомкам

Константы
---------

.. code-block:: python

   INTERNAL_UPDATE_TYPES: frozenset[str] = frozenset({"update", "error"})

Исходный файл
--------------

``maxgram/dispatcher/router.py``
