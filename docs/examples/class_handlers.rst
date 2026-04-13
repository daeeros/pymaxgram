========================
Классовые обработчики
========================

.. code-block:: python

   import asyncio
   from maxgram import Bot, Dispatcher, Router
   from maxgram.filters import Command
   from maxgram.handlers import (
       MessageHandler,
       MessageHandlerCommandMixin,
       CallbackHandler,
       ErrorHandler,
   )

   bot = Bot(token="YOUR_BOT_TOKEN")
   dp = Dispatcher()
   router = Router()

   # Обработчик сообщений
   class EchoHandler(MessageHandler):
       async def handle(self):
           text = self.event.body.text or "No text"
           await self.event.answer(text=f"Echo: {text}")

   # Обработчик команд с миксином
   class HelpHandler(MessageHandlerCommandMixin, MessageHandler):
       async def handle(self):
           name = self.from_user.first_name if self.from_user else "User"
           await self.event.answer(
               text=f"Hello, {name}!\n"
               f"Available commands: /help, /echo"
           )

   # Обработчик callback
   class ButtonHandler(CallbackHandler):
       async def handle(self):
           user = self.from_user.first_name
           await self.event.answer(
               notification=f"{user} clicked a button!"
           )

   # Обработчик ошибок
   class GlobalErrorHandler(ErrorHandler):
       async def handle(self):
           print(
               f"Error: {self.exception_name}: "
               f"{self.exception_message}"
           )

   # Регистрация
   router.message.register(HelpHandler, Command("help"))
   router.message.register(EchoHandler)
   router.message_callback.register(ButtonHandler)
   router.error.register(GlobalErrorHandler)

   dp.include_router(router)
   asyncio.run(dp.start_polling(bot))
