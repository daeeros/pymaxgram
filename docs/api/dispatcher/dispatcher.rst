============
Dispatcher
============

.. module:: maxgram.dispatcher.dispatcher

Корневой роутер, управляющий polling/webhook и middleware.

.. code-block:: python

   class Dispatcher(Router):
       def __init__(
           self,
           *,
           storage: BaseStorage | None = None,
           fsm_strategy: FSMStrategy = FSMStrategy.USER_IN_CHAT,
           events_isolation: BaseEventIsolation | None = None,
           disable_fsm: bool = False,
           updates_debug: bool = False,
           requests_debug: bool = False,
           name: str | None = None,
           **kwargs: Any,
       ) -> None: ...

Дополнительные атрибуты
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Атрибут
     - Тип
     - Описание
   * - ``update``
     - ``MaxEventObserver``
     - Наблюдатель корневого события ``update``
   * - ``fsm``
     - ``FSMContextMiddleware``
     - FSM middleware
   * - ``workflow_data``
     - ``dict[str, Any]``
     - Данные, передаваемые в обработчики
   * - ``storage``
     - ``BaseStorage``
     - Хранилище FSM (свойство)
   * - ``updates_debug``
     - ``bool``
     - Логировать входящие update (``False``)
   * - ``requests_debug``
     - ``bool``
     - Логировать исходящие API-запросы (``False``)

Dict-интерфейс
--------------

.. code-block:: python

   dp["key"] = value          # __setitem__
   value = dp["key"]          # __getitem__
   del dp["key"]              # __delitem__
   value = dp.get("key")      # get с default

Методы polling
--------------

start_polling
^^^^^^^^^^^^^

.. code-block:: python

   async def start_polling(
       self,
       *bots: Bot,
       polling_timeout: int = 10,
       handle_as_tasks: bool = True,
       backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
       allowed_updates: list[str] | UNSET_TYPE | None = UNSET,
       handle_signals: bool = True,
       close_bot_session: bool = True,
       tasks_concurrency_limit: int | None = None,
       **kwargs: Any,
   ) -> None

run_polling
^^^^^^^^^^^

.. code-block:: python

   def run_polling(self, *bots, **kwargs) -> None

Блокирующая версия ``start_polling``. Автоматически использует ``uvloop`` если доступен.

stop_polling
^^^^^^^^^^^^

.. code-block:: python

   async def stop_polling(self) -> None

Методы webhook
--------------

feed_update
^^^^^^^^^^^

.. code-block:: python

   async def feed_update(
       self, bot: Bot, update: Update, **kwargs,
   ) -> Any

Обрабатывает одно обновление через middleware-цепочку.

feed_raw_update
^^^^^^^^^^^^^^^

.. code-block:: python

   async def feed_raw_update(
       self, bot: Bot, update: dict[str, Any], **kwargs,
   ) -> Any

Парсит dict в Update и обрабатывает.

feed_webhook_update
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   async def feed_webhook_update(
       self, bot: Bot, update: Update | dict, _timeout: float = 55, **kwargs,
   ) -> None

Встроенные middleware (outer на update)
---------------------------------------

1. ``ErrorsMiddleware(self)``
2. ``UserContextMiddleware()``
3. ``FSMContextMiddleware(storage, strategy, events_isolation)``

Константы
---------

.. code-block:: python

   DEFAULT_BACKOFF_CONFIG = BackoffConfig(
       min_delay=1.0, max_delay=5.0, factor=1.3, jitter=0.1,
   )

Исходный файл
--------------

``maxgram/dispatcher/dispatcher.py``
