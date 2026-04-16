# CallbackData (фабрика)

Структурированные callback-данные.

```python
import asyncio
from maxgram import Bot, Dispatcher, Router
from maxgram.filters import CallbackData, Command
from maxgram.utils.keyboard import InlineKeyboardBuilder

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()
router = Router()

# Определение структуры
class ProductCallback(CallbackData, prefix="product"):
    id: int
    action: str

@router.message(Command("products"))
async def show_products(message, bot):
    builder = InlineKeyboardBuilder()
    builder.callback(
        text="Buy iPhone",
        callback_data=ProductCallback(id=1, action="buy"),
    )
    builder.callback(
        text="Info MacBook",
        callback_data=ProductCallback(id=2, action="info"),
    )

    await message.answer("Our products:", keyboard=builder)

@router.message_callback(ProductCallback.filter())
async def on_product(callback, callback_data: ProductCallback, bot):
    if callback_data.action == "buy":
        await callback.answer(
            notification=f"Buying product #{callback_data.id}..."
        )
    elif callback_data.action == "info":
        await callback.answer(
            text=f"Product #{callback_data.id}: MacBook Pro 16"
        )

dp.include_router(router)
asyncio.run(dp.start_polling(bot))
```
