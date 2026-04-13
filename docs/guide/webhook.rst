==============
Webhook-режим
==============

Помимо long polling, pymaxgram поддерживает получение обновлений через webhook.

Настройка webhook
-----------------

.. code-block:: python

   from aiohttp import web
   from maxgram import Bot, Dispatcher
   from maxgram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

   bot = Bot(token="YOUR_BOT_TOKEN")
   dp = Dispatcher()

   # ... регистрация обработчиков ...

   app = web.Application()
   handler = SimpleRequestHandler(dp, bot, secret_token="your_secret")
   handler.register(app, "/webhook")
   setup_application(app, dp)
   web.run_app(app, host="0.0.0.0", port=8080)

Компоненты
----------

setup_application
^^^^^^^^^^^^^^^^^

Привязывает жизненный цикл Dispatcher к приложению aiohttp:

.. code-block:: python

   setup_application(app, dp, **kwargs)

- Вызывает ``dp.emit_startup()`` при старте приложения
- Вызывает ``dp.emit_shutdown()`` при остановке

SimpleRequestHandler
^^^^^^^^^^^^^^^^^^^^

Обработчик HTTP-запросов для одного бота:

.. code-block:: python

   handler = SimpleRequestHandler(
       dispatcher=dp,
       bot=bot,
       secret_token="your_secret",  # Опционально
   )
   handler.register(app, "/webhook")

- Проверяет заголовок ``X-Max-Bot-Api-Secret`` если задан ``secret_token``
- Парсит JSON-тело запроса как Update
- Передаёт обновление в Dispatcher

BaseRequestHandler
^^^^^^^^^^^^^^^^^^

Абстрактный базовый класс для пользовательских обработчиков webhook:

.. code-block:: python

   from maxgram.webhook.aiohttp_server import BaseRequestHandler

   class MyHandler(BaseRequestHandler):
       async def resolve_bot(self, request) -> Bot:
           # Логика определения бота (для мультибот-режима)
           return self.bot

       async def handle(self, request) -> web.Response:
           # Кастомная обработка
           ...

Регистрация webhook
-------------------

Перед запуском webhook-сервера нужно зарегистрировать подписку:

.. code-block:: python

   # В startup-обработчике
   @router.startup()
   async def on_startup(bot, dispatcher):
       await bot.create_subscription(
           url="https://your-domain.com/webhook",
           update_types=["message_created", "message_callback", "bot_started"],
           secret="your_secret",
       )

   @router.shutdown()
   async def on_shutdown(bot, dispatcher):
       await bot.delete_subscription(url="https://your-domain.com/webhook")

IP-фильтрация
--------------

Для безопасности можно ограничить IP-адреса, с которых принимаются webhook-запросы:

.. code-block:: python

   from maxgram.webhook.security import IPFilter, ip_filter_middleware

   # Разрешённые IP
   ip_filter = IPFilter(ips=["1.2.3.4", "5.6.7.8"])

   # Как middleware aiohttp
   app.middlewares.append(ip_filter_middleware(ip_filter))

Polling vs Webhook
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * -
     - Polling
     - Webhook
   * - **Простота**
     - Проще настроить
     - Нужен домен + SSL
   * - **Задержка**
     - Зависит от timeout
     - Мгновенная доставка
   * - **Нагрузка**
     - Постоянные запросы к API
     - Запросы только при событиях
   * - **Для разработки**
     - Подходит
     - Нужен публичный URL
   * - **Для продакшена**
     - Для малых нагрузок
     - Рекомендуется
