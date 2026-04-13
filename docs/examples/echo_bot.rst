===========
Эхо-бот
===========

Минимальный бот, который повторяет текст каждого сообщения.

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

С блокирующим запуском
----------------------

.. code-block:: python

   from maxgram import Bot, Dispatcher, Router

   bot = Bot(token="YOUR_BOT_TOKEN")
   dp = Dispatcher()
   router = Router()

   @router.message()
   async def echo(message, bot):
       await message.answer(text=message.body.text)

   dp.include_router(router)
   dp.run_polling(bot)  # Автоматически использует uvloop если установлен

С логированием
--------------

.. code-block:: python

   import asyncio
   import logging
   from maxgram import Bot, Dispatcher, Router

   logging.basicConfig(level=logging.INFO)

   bot = Bot(token="YOUR_BOT_TOKEN")
   dp = Dispatcher()
   router = Router()

   @router.startup()
   async def on_startup(bot, dispatcher):
       me = await bot.get_me()
       logging.info("Bot started: %s (@%s)", me.first_name, me.username)

   @router.message()
   async def echo(message, bot):
       await message.answer(text=message.body.text)

   dp.include_router(router)
   asyncio.run(dp.start_polling(bot))
