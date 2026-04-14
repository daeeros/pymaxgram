==============
Быстрый старт
==============

В этом руководстве мы создадим простого эхо-бота, который отвечает на каждое сообщение.

Получение токена
----------------

Для работы бота вам нужен токен. Получите его в настройках MAX Messenger через
раздел создания ботов.

Минимальный бот
---------------

Создайте файл ``bot.py``:

.. code-block:: python

   import asyncio
   from maxgram import Bot, Dispatcher, Router

   # Создаём экземпляры
   bot = Bot(token="YOUR_BOT_TOKEN")
   dp = Dispatcher()
   router = Router()

   # Регистрируем обработчик всех сообщений
   @router.message()
   async def echo(message, bot):
       await message.answer(text=message.body.text)

   # Подключаем роутер и запускаем polling
   dp.include_router(router)
   asyncio.run(dp.start_polling(bot))

Запустите:

.. code-block:: bash

   python bot.py

Разбор кода
-----------

1. **Bot** — HTTP-клиент для взаимодействия с MAX Bot API. Принимает токен аутентификации.

2. **Dispatcher** — корневой маршрутизатор, управляющий циклом polling и распределением событий.

3. **Router** — маршрутизатор для регистрации обработчиков. Можно создавать несколько роутеров для модульной архитектуры.

4. **@router.message()** — декоратор для регистрации обработчика входящих сообщений. Без аргументов — обрабатывает все сообщения.

5. **message.answer()** — отправляет ответ в тот же чат, откуда пришло сообщение.

6. **dp.include_router(router)** — подключает роутер к диспетчеру.

7. **dp.start_polling(bot)** — запускает long polling для получения обновлений.

Добавляем команды
-----------------

.. code-block:: python

   import asyncio
   from maxgram import Bot, Dispatcher, Router
   from maxgram.filters import Command
   from maxgram.types import BotStarted

   bot = Bot(token="YOUR_BOT_TOKEN")
   dp = Dispatcher()
   router = Router()

   @router.bot_started()
   async def start(event: BotStarted):
       await event.answer(text=f"Привет, {event.user.first_name}! Я эхо-бот.")

   @router.message(Command("help"))
   async def help_cmd(message, bot):
       await message.answer(text="Доступные команды:\n/start — Запуск\n/help — Справка")

   @router.message()
   async def echo(message, bot):
       await message.answer(text=message.body.text)

   dp.include_router(router)
   asyncio.run(dp.start_polling(bot))

.. important::

   Порядок регистрации обработчиков важен. Обработчики проверяются сверху вниз —
   первый совпавший фильтр обрабатывает событие. Поэтому ``echo`` (без фильтров)
   должен быть последним.

Структура проекта
-----------------

Для более сложных ботов рекомендуется такая структура:

.. code-block:: text

   my_bot/
   ├── bot.py              # Точка входа
   ├── config.py           # Конфигурация (токен и т.д.)
   ├── handlers/
   │   ├── __init__.py
   │   ├── start.py        # Команды /start, /help
   │   ├── messages.py     # Обработка сообщений
   │   └── callbacks.py    # Обработка callback
   ├── keyboards/
   │   └── inline.py       # Inline-клавиатуры
   ├── states/
   │   └── registration.py # FSM-состояния
   └── middlewares/
       └── auth.py         # Middleware авторизации

Что дальше?
-----------

- :doc:`/guide/bot` — подробнее о классе Bot и его методах
- :doc:`/guide/dispatcher` — Dispatcher и Router
- :doc:`/guide/filters` — система фильтров
- :doc:`/guide/keyboards` — inline-клавиатуры
- :doc:`/guide/fsm` — конечные автоматы
- :doc:`/examples/index` — полные примеры
