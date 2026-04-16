# Загрузка файлов

```python
import asyncio
from maxgram import Bot, Dispatcher, Router
from maxgram.filters import Command
from maxgram.types import Attachment

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()
router = Router()

@router.message(Command("photo"))
async def send_photo(message, bot):
    # Загрузка из байтов
    with open("photo.jpg", "rb") as f:
        file_data = f.read()

    token = await bot.upload_file(
        file_type="image",
        file_data=file_data,
        filename="photo.jpg",
    )

    await message.answer(
        text="Here is your photo:",
        attachments=[
            Attachment(type="image", payload={"token": token}),
        ],
    )

@router.message(Command("file"))
async def send_file(message, bot):
    content = b"Hello from pymaxgram!"
    token = await bot.upload_file(
        file_type="file",
        file_data=content,
        filename="hello.txt",
    )

    await message.answer(
        text="File attached:",
        attachments=[
            Attachment(type="file", payload={"token": token}),
        ],
    )

dp.include_router(router)
asyncio.run(dp.start_polling(bot))
```
