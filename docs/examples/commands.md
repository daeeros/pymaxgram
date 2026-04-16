# Команды

Обработка текстовых команд с аргументами.

```python
import asyncio
from maxgram import Bot, Dispatcher, Router
from maxgram.filters import Command, CommandObject
from maxgram.types import BotStarted

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()
router = Router()

@router.bot_started()
async def start(event: BotStarted):
    await event.answer(text=f"Welcome, {event.user.first_name}!")

@router.message(Command("help"))
async def help_cmd(message, bot):
    await message.answer(
        text="Available commands:\n"
        "/start - Start bot\n"
        "/help - Show help\n"
        "/echo <text> - Echo text\n"
        "/upper <text> - Uppercase text"
    )

@router.message(Command("echo"))
async def echo_cmd(message, command: CommandObject, bot):
    if command.args:
        await message.answer(text=command.args)
    else:
        await message.answer(text="Usage: /echo <text>")

@router.message(Command("upper"))
async def upper_cmd(message, command: CommandObject, bot):
    if command.args:
        await message.answer(text=command.args.upper())
    else:
        await message.answer(text="Usage: /upper <text>")

@router.message()
async def fallback(message, bot):
    await message.answer(text="Unknown command. Try /help")

dp.include_router(router)
asyncio.run(dp.start_polling(bot))
```
