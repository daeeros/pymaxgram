# Форматирование текста

```python
import asyncio
from maxgram import Bot, Dispatcher, Router
from maxgram.filters import Command
from maxgram.utils.formatting import (
    Bold, Code, Italic, Pre, Text,
    as_list, as_marked_list, as_numbered_list, as_section,
)

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()
router = Router()

@router.message(Command("format"))
async def format_example(message, bot):
    content = as_list(
        Bold("User Info"),
        as_marked_list(
            f"Name: {message.sender.first_name}",
            f"ID: {message.sender.user_id}",
            f"Bot: {message.sender.is_bot}",
        ),
        "",
        as_section(
            Bold("Features"),
            as_numbered_list(
                "Async architecture",
                "FSM support",
                "Middleware system",
                "Inline keyboards",
            ),
        ),
    )
    await message.answer(**content.as_kwargs())

@router.message(Command("code"))
async def code_example(message, bot):
    content = as_list(
        Bold("Code Example:"),
        Pre('from maxgram import Bot\nbot = Bot(token="...")'),
        "",
        Text("Use ", Code("/help"), " for more info."),
    )
    await message.answer(**content.as_kwargs())

@router.message(Command("styled"))
async def styled(message, bot):
    content = Text(
        Bold("Bold"), ", ",
        Italic("italic"), ", ",
        Code("code"), ", ",
        Bold(Italic("bold italic")),
    )
    await message.answer(**content.as_kwargs())

dp.include_router(router)
asyncio.run(dp.start_polling(bot))
```
