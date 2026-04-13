=======================
Dispatcher и Router
=======================

Dispatcher и Router — основа системы маршрутизации событий в pymaxgram.

Router
------

:class:`~maxgram.Router` — маршрутизатор событий. Позволяет регистрировать
обработчики для различных типов событий.

Создание
^^^^^^^^

.. code-block:: python

   from maxgram import Router

   router = Router(name="my_router")  # name опционален

Наблюдатели событий (observers)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Каждый роутер содержит наблюдатели для трёх типов событий MAX API:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Наблюдатель
     - Тип события
     - Описание
   * - ``router.message``
     - ``message_created``
     - Входящие сообщения
   * - ``router.message_callback``
     - ``message_callback``
     - Нажатия inline-кнопок
   * - ``router.bot_started``
     - ``bot_started``
     - Запуск бота пользователем
   * - ``router.error``
     - ``error``
     - Ошибки обработки

Дополнительные наблюдатели жизненного цикла:

- ``router.startup`` — событие запуска
- ``router.shutdown`` — событие остановки

Регистрация обработчиков
^^^^^^^^^^^^^^^^^^^^^^^^

Через декораторы:

.. code-block:: python

   @router.message()
   async def handle_message(message, bot):
       await message.answer(text="Got it!")

   @router.message_callback()
   async def handle_callback(callback, bot):
       await callback.answer(notification="Clicked!")

   @router.bot_started()
   async def handle_start(event, bot):
       pass

   @router.error()
   async def handle_error(error, bot):
       pass

   @router.startup()
   async def on_startup(bot, dispatcher):
       print("Bot started!")

   @router.shutdown()
   async def on_shutdown(bot, dispatcher):
       print("Bot stopped!")

С фильтрами:

.. code-block:: python

   from maxgram.filters import Command, StateFilter
   from maxgram import F

   @router.message(Command("help"))
   async def help_cmd(message, bot):
       pass

   @router.message(F.body.text == "hello")
   async def hello(message, bot):
       pass

   @router.message_callback(F.payload.startswith("action:"))
   async def action(callback, bot):
       pass

Вложенные роутеры
^^^^^^^^^^^^^^^^^

Роутеры можно вкладывать друг в друга для модульной архитектуры:

.. code-block:: python

   from maxgram import Router

   main_router = Router(name="main")
   admin_router = Router(name="admin")
   user_router = Router(name="user")

   # Подключение одного роутера
   main_router.include_router(admin_router)

   # Подключение нескольких
   main_router.include_routers(admin_router, user_router)

.. important::

   - Роутер может быть подключён только к одному родителю
   - Циклические ссылки запрещены
   - Событие проходит по дереву сверху вниз: сначала проверяются обработчики
     текущего роутера, затем дочерних

Порядок обработки событий
^^^^^^^^^^^^^^^^^^^^^^^^^

1. Проверяются root-фильтры наблюдателя
2. Проверяются обработчики текущего роутера (в порядке регистрации)
3. Если ни один обработчик не сработал — событие передаётся дочерним роутерам
4. Первый совпавший обработчик обрабатывает событие

Dispatcher
----------

:class:`~maxgram.Dispatcher` — корневой роутер, управляющий циклом получения
обновлений и их распределением.

Создание
^^^^^^^^

.. code-block:: python

   from maxgram import Dispatcher
   from maxgram.fsm.storage.memory import MemoryStorage
   from maxgram.fsm.strategy import FSMStrategy

   # Минимальный
   dp = Dispatcher()

   # С настройками FSM
   dp = Dispatcher(
       storage=MemoryStorage(),
       fsm_strategy=FSMStrategy.USER_IN_CHAT,
       disable_fsm=False,
       name="main",
   )

Параметры конструктора
^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Параметр
     - Тип
     - Описание
   * - ``storage``
     - ``BaseStorage | None``
     - Хранилище FSM. По умолчанию ``MemoryStorage()``
   * - ``fsm_strategy``
     - ``FSMStrategy``
     - Стратегия FSM. По умолчанию ``USER_IN_CHAT``
   * - ``events_isolation``
     - ``BaseEventIsolation | None``
     - Изоляция событий для конкурентности
   * - ``disable_fsm``
     - ``bool``
     - Отключить FSM middleware (``False``)
   * - ``updates_debug``
     - ``bool``
     - Логировать все входящие update в читаемом виде (``False``)
   * - ``requests_debug``
     - ``bool``
     - Логировать все исходящие API-запросы (``False``)
   * - ``name``
     - ``str | None``
     - Имя диспетчера
   * - ``**kwargs``
     - ``Any``
     - Данные workflow (доступны в обработчиках)

Встроенные middleware
^^^^^^^^^^^^^^^^^^^^

Dispatcher автоматически регистрирует три outer middleware на наблюдателе ``update``:

1. **ErrorsMiddleware** — перехватывает исключения и направляет их в обработчики ошибок
2. **UserContextMiddleware** — извлекает контекст пользователя/чата из обновления
3. **FSMContextMiddleware** — предоставляет FSM-контекст в обработчики

Long Polling
^^^^^^^^^^^^

.. code-block:: python

   import asyncio
   from maxgram import Bot, Dispatcher

   bot = Bot(token="TOKEN")
   dp = Dispatcher()

   # Вариант 1: async
   asyncio.run(dp.start_polling(bot))

   # Вариант 2: блокирующий (с поддержкой uvloop)
   dp.run_polling(bot)

Параметры ``start_polling()``:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Параметр
     - Тип
     - Описание
   * - ``*bots``
     - ``Bot``
     - Один или несколько экземпляров Bot
   * - ``polling_timeout``
     - ``int``
     - Таймаут long polling (по умолчанию 10 сек)
   * - ``handle_as_tasks``
     - ``bool``
     - Обрабатывать обновления в отдельных задачах (``True``)
   * - ``backoff_config``
     - ``BackoffConfig``
     - Настройки экспоненциального отступления при ошибках
   * - ``allowed_updates``
     - ``list[str] | None``
     - Список типов обновлений. По умолчанию — автоопределение
   * - ``handle_signals``
     - ``bool``
     - Обрабатывать SIGINT/SIGTERM (``True``)
   * - ``close_bot_session``
     - ``bool``
     - Закрывать сессию бота при остановке (``True``)
   * - ``tasks_concurrency_limit``
     - ``int | None``
     - Лимит параллельных задач обработки

Workflow Data
^^^^^^^^^^^^^

Dispatcher поддерживает хранение данных, доступных во всех обработчиках:

.. code-block:: python

   dp = Dispatcher()

   # Через конструктор
   dp = Dispatcher(db=database, config=settings)

   # Через dict-интерфейс
   dp["db"] = database
   dp["config"] = settings

   # Доступ в обработчике
   @router.message()
   async def handler(message, bot, db, config):
       # db и config автоматически инъектируются
       pass

Webhook-режим
^^^^^^^^^^^^^

.. code-block:: python

   await dp.feed_webhook_update(bot, update)
   await dp.feed_raw_update(bot, raw_dict)

Остановка
^^^^^^^^^

.. code-block:: python

   await dp.stop_polling()

Многоботовый режим
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   bot1 = Bot(token="TOKEN_1")
   bot2 = Bot(token="TOKEN_2")

   dp = Dispatcher()
   # Оба бота используют одни и те же обработчики
   await dp.start_polling(bot1, bot2)

Режим отладки
^^^^^^^^^^^^^

.. code-block:: python

   dp = Dispatcher(
       updates_debug=True,     # Логировать входящие update
       requests_debug=True,    # Логировать исходящие API-запросы
   )

``updates_debug=True`` выводит для каждого update:

.. code-block:: text

   ============================================================
   UPDATE message_callback
     from: Michael (id=248173258)
     payload: 'adm:plg:'
     callback_id: f9LHodD0cOKe8x...
     message_mid: mid.ffffbd399a199736
   ============================================================
     -> HANDLED in 15 ms (type=message_callback)

``requests_debug=True`` выводит для каждого API-вызова:

.. code-block:: text

   POST /answers params={'callback_id': 'abc'} body={'message': {'text': '...'}}
     -> bool
