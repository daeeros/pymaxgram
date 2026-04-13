==================
Inline-клавиатуры
==================

Создание и обработка inline-клавиатур.

С InlineKeyboardBuilder (рекомендуется)
----------------------------------------

.. code-block:: python

   import asyncio
   from maxgram import Bot, Dispatcher, F, Router
   from maxgram.filters import Command
   from maxgram.utils.keyboard import InlineKeyboardBuilder

   bot = Bot(token="YOUR_BOT_TOKEN")
   dp = Dispatcher()
   router = Router()

   @router.message(Command("menu"))
   async def show_menu(message, bot):
       builder = InlineKeyboardBuilder()
       builder.button(text="Like", payload="vote:like")
       builder.button(text="Dislike", payload="vote:dislike")
       builder.adjust(2)

       await message.answer("Rate our bot:", keyboard=builder)

   @router.message_callback(F.payload == "vote:like")
   async def on_like(callback, bot):
       await callback.answer(notification="Thanks for your like!")

   @router.message_callback(F.payload == "vote:dislike")
   async def on_dislike(callback, bot):
       await callback.answer(notification="We'll try to improve!")

   dp.include_router(router)
   asyncio.run(dp.start_polling(bot))

С InlineKeyboard напрямую
--------------------------

.. code-block:: python

   from maxgram.types import InlineKeyboard, Button
   from maxgram.enums import ButtonType

   @router.message(Command("links"))
   async def show_links(message, bot):
       keyboard = InlineKeyboard(buttons=[
           [
               Button(type=ButtonType.CALLBACK, text="Click", payload="btn:1"),
           ],
           [
               Button(type=ButtonType.LINK, text="Website", url="https://max.ru"),
           ],
       ])
       await message.answer("Links:", keyboard=keyboard)
