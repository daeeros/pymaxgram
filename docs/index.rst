==================================
pymaxgram — документация
==================================

.. image:: https://img.shields.io/pypi/v/pymaxgram.svg
   :target: https://pypi.org/project/pymaxgram/

.. image:: https://img.shields.io/pypi/pyversions/pymaxgram.svg
   :target: https://pypi.org/project/pymaxgram/

.. image:: https://img.shields.io/github/license/daeeros/pymaxgram.svg
   :target: https://github.com/daeeros/pymaxgram/blob/main/LICENSE

**pymaxgram** — асинхронный Python-фреймворк для создания ботов на платформе `MAX Messenger <https://max.ru>`_.

Построен на базе ``asyncio``, ``aiohttp`` и ``pydantic``. Вдохновлён архитектурой `aiogram <https://aiogram.dev>`_.

Быстрый старт
--------------

.. code-block:: python

   import asyncio
   from maxgram import Bot, Dispatcher, Router

   bot = Bot(token="YOUR_BOT_TOKEN")
   dp = Dispatcher()
   router = Router()

   @router.message()
   async def echo(message, bot):
       await message.answer(text=message.body.text)

   dp.include_router(router)
   asyncio.run(dp.start_polling(bot))

Возможности
-----------

- Полностью асинхронный (asyncio + aiohttp)
- Типизация данных через Pydantic v2
- Система фильтров (команды, callback data, FSM-состояния, magic filter)
- Конечные автоматы (FSM) с поддержкой стратегий
- Middleware на уровне запросов и событий
- Inline-клавиатуры и обработка callback
- Форматирование текста (HTML / Markdown)
- Загрузка файлов (из памяти, файловой системы, URL)
- Webhook-режим через aiohttp
- Модульная архитектура с вложенными роутерами

Содержание
----------

.. toctree::
   :maxdepth: 2
   :caption: Начало работы

   getting-started/index
   getting-started/installation
   getting-started/quickstart

.. toctree::
   :maxdepth: 2
   :caption: Руководство

   guide/index
   guide/bot
   guide/dispatcher
   guide/handlers
   guide/filters
   guide/keyboards
   guide/fsm
   guide/middlewares
   guide/formatting
   guide/files
   guide/webhook
   guide/errors

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index
   api/client/bot
   api/client/session
   api/client/default
   api/types/index
   api/types/base
   api/types/user
   api/types/chat
   api/types/message
   api/types/callback
   api/types/update
   api/types/attachments
   api/types/keyboard
   api/types/input_file
   api/types/other
   api/methods/index
   api/methods/base
   api/methods/messages
   api/methods/chats
   api/methods/members
   api/methods/admins
   api/methods/callbacks
   api/methods/subscriptions
   api/methods/updates
   api/methods/uploads
   api/methods/pins
   api/methods/actions
   api/methods/bot_info
   api/dispatcher/router
   api/dispatcher/dispatcher
   api/dispatcher/event
   api/dispatcher/middlewares
   api/filters/index
   api/filters/base
   api/filters/command
   api/filters/callback_data
   api/filters/state
   api/filters/other
   api/fsm/state
   api/fsm/context
   api/fsm/storage
   api/fsm/strategy
   api/handlers/index
   api/enums/index
   api/utils/index
   api/utils/keyboard_builder
   api/utils/chat_action
   api/utils/formatting
   api/utils/backoff
   api/utils/other
   api/exceptions
   api/webhook/index

.. toctree::
   :maxdepth: 2
   :caption: Примеры

   examples/index
   examples/echo_bot
   examples/commands
   examples/keyboards
   examples/callback_data
   examples/fsm
   examples/middleware
   examples/files
   examples/formatting
   examples/class_handlers

Индексы
-------

* :ref:`genindex`
* :ref:`search`
