# pymaxgram

Async Python framework for building bots on **MAX Messenger** platform.

Built with `asyncio`, `aiohttp`, and `pydantic`.

## Installation

```bash
pip install pymaxgram
```

## Quick Start

```python
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
```

---

## Examples

### Command Handling

```python
from maxgram.filters import Command, CommandObject
from maxgram.types import BotStarted

router = Router()


@router.bot_started()
async def start_handler(event: BotStarted, bot):
    await bot.send_message(user_id=event.user.user_id, text=f"Welcome, {event.user.first_name}!")


@router.message(Command("help"))
async def help_handler(message, bot):
    await message.answer(text="Available commands:\n/start - Start bot\n/help - Show help")


@router.message(Command("echo"))
async def echo_command(message, command: CommandObject, bot):
    if command.args:
        await message.answer(text=command.args)
    else:
        await message.answer(text="Usage: /echo <text>")
```

### Inline Keyboard & Callbacks

```python
from maxgram import F, Router
from maxgram.filters import Command
from maxgram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(Command("menu"))
async def show_menu(message, bot):
    builder = InlineKeyboardBuilder()
    builder.callback(text="Like", payload="vote:like")
    builder.callback(text="Dislike", payload="vote:dislike")
    builder.adjust(2)

    await message.answer("Rate our bot:", keyboard=builder)


@router.message_callback(F.payload == "vote:like")
async def on_like(callback, bot):
    await callback.answer(notification="Thanks for your like!")


@router.message_callback(F.payload == "vote:dislike")
async def on_dislike(callback, bot):
    await callback.answer(notification="We'll try to improve!")
```

### CallbackData Factory

```python
from maxgram import F, Router
from maxgram.filters import CallbackData, Command
from maxgram.utils.keyboard import InlineKeyboardBuilder

router = Router()


class ProductCallback(CallbackData, prefix="product"):
    id: int
    action: str


@router.message(Command("products"))
async def show_products(message, bot):
    builder = InlineKeyboardBuilder()
    builder.callback(text="Buy iPhone", callback_data=ProductCallback(id=1, action="buy"))
    builder.callback(text="Buy MacBook", callback_data=ProductCallback(id=2, action="buy"))

    await message.answer("Our products:", keyboard=builder)


@router.message_callback(ProductCallback.filter())
async def on_product_action(callback, callback_data: ProductCallback, bot):
    await callback.answer(
        notification=f"Product #{callback_data.id}, action: {callback_data.action}"
    )
```

### Finite State Machine (FSM)

```python
from maxgram import Bot, Dispatcher, Router
from maxgram.filters import Command, StateFilter
from maxgram.fsm.state import State, StatesGroup
from maxgram.fsm.context import FSMContext

router = Router()


class RegistrationStates(StatesGroup):
    waiting_name = State()
    waiting_age = State()


@router.message(Command("register"))
async def start_registration(message, state: FSMContext, bot):
    await state.set_state(RegistrationStates.waiting_name)
    await message.answer(text="What is your name?")


@router.message(StateFilter(RegistrationStates.waiting_name))
async def process_name(message, state: FSMContext, bot):
    await state.update_data(name=message.body.text)
    await state.set_state(RegistrationStates.waiting_age)
    await message.answer(text="How old are you?")


@router.message(StateFilter(RegistrationStates.waiting_age))
async def process_age(message, state: FSMContext, bot):
    try:
        age = int(message.body.text)
    except ValueError:
        await message.answer(text="Please enter a valid number.")
        return

    await state.update_data(age=age)
    data = await state.get_data()
    await state.clear()
    await message.answer(text=f"Registration complete!\nName: {data['name']}\nAge: {age}")
```

### MagicFilter

```python
from maxgram import F, Router

router = Router()

# Filter messages by text content
@router.message(F.body.text == "hello")
async def exact_match(message, bot):
    await message.answer(text="Hello!")


# Filter by sender
@router.message(F.sender.is_bot == False)
async def humans_only(message, bot):
    pass


# Filter callbacks by payload prefix
@router.message_callback(F.payload.startswith("action:"))
async def action_handler(callback, bot):
    action = callback.payload.split(":")[1]
    await callback.answer(notification=f"Action: {action}")
```

### Middleware

```python
import time
import logging
from typing import Any
from collections.abc import Awaitable, Callable

from maxgram import BaseMiddleware
from maxgram.types import MaxObject

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[MaxObject, dict[str, Any]], Awaitable[Any]],
        event: MaxObject,
        data: dict[str, Any],
    ) -> Any:
        start = time.monotonic()
        result = await handler(event, data)
        duration = time.monotonic() - start
        logger.info("Handler completed in %.3fs", duration)
        return result


class AuthMiddleware(BaseMiddleware):
    def __init__(self, allowed_user_ids: set[int]):
        self.allowed_user_ids = allowed_user_ids

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        if user and user.user_id not in self.allowed_user_ids:
            return  # Ignore unauthorized users
        return await handler(event, data)


# Register middleware on router
router.message.outer_middleware(LoggingMiddleware())
router.message.outer_middleware(AuthMiddleware(allowed_user_ids={123456, 789012}))
```

### Chat Actions (Typing Indicator)

```python
import asyncio
from maxgram import Router
from maxgram.utils.chat_action import ChatActionSender
from maxgram.filters import Command

router = Router()


@router.message(Command("slow"))
async def slow_handler(message, bot):
    async with ChatActionSender.typing(
        chat_id=message.recipient.chat_id,
        bot=bot,
    ):
        await asyncio.sleep(3)  # Simulate long operation
        await message.answer(text="Done! Typing indicator was shown while processing.")
```

### Text Formatting

```python
from maxgram import Router
from maxgram.utils.formatting import (
    Text, Bold, Italic, Code, Pre, TextLink, UserMention,
    as_list, as_marked_list, as_numbered_list, as_section,
)
from maxgram.filters import Command

router = Router()


@router.message(Command("format"))
async def formatting_example(message, bot):
    content = as_list(
        Bold("User Info"),
        as_marked_list(
            f"Name: {message.sender.first_name}",
            f"ID: {message.sender.user_id}",
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
        Pre("print('Hello, MAX!')"),
        "",
        Text("Use ", Code("/help"), " for more info."),
    )
    await message.answer(**content.as_kwargs())
```

### Event Handling (all 15 update types)

Each event type has its own typed class with proper fields:

```python
from maxgram import Router
from maxgram.types import (
    Message, Callback,
    BotStarted, BotStopped, BotAdded, BotRemoved,
    UserAdded, UserRemoved, ChatTitleChanged,
    MessageRemoved, DialogMuted,
)

router = Router()

# Bot lifecycle
@router.bot_started()
async def on_start(event: BotStarted, bot):
    print(f"{event.user.first_name} started the bot")
    if event.payload:
        print(f"Raw payload: {event.payload}")
        print(f"Decoded deep link: {event.deep_link()}")

@router.bot_stopped()
async def on_stop(event: BotStopped, bot):
    print(f"{event.user.first_name} stopped the bot")

# Bot added/removed from chat
@router.bot_added()
async def on_bot_added(event: BotAdded, bot):
    print(f"Bot added to {'channel' if event.is_channel else 'chat'} {event.chat_id}")

@router.bot_removed()
async def on_bot_removed(event: BotRemoved, bot):
    print(f"Bot removed from chat {event.chat_id}")

# User management
@router.user_added()
async def on_user_added(event: UserAdded, bot):
    print(f"{event.user.first_name} joined chat {event.chat_id}")
    if event.inviter_id:
        print(f"Invited by {event.inviter_id}")

@router.user_removed()
async def on_user_removed(event: UserRemoved, bot):
    print(f"{event.user.first_name} left chat {event.chat_id}")

# Message events
@router.message_edited()
async def on_edit(message: Message, bot):
    print(f"Message edited: {message.body.mid}")

@router.message_removed()
async def on_removed(event: MessageRemoved, bot):
    print(f"Message {event.message_id} removed from {event.chat_id}")

# Chat events
@router.chat_title_changed()
async def on_title(event: ChatTitleChanged, bot):
    print(f"Chat {event.chat_id} renamed to: {event.title}")

# Dialog events
@router.dialog_muted()
async def on_muted(event: DialogMuted, bot):
    print(f"Dialog muted until {event.muted_until}")
```

### Deep Links

```python
from maxgram import F, Router
from maxgram.types import BotStarted
from maxgram.utils.payload import encode_payload, decode_payload

router = Router()

# --- Creating deep links ---
# Plain: https://max.ru/your_bot?start=promo_summer
# Encoded: https://max.ru/your_bot?start=c2VjcmV0X2RhdGE
encoded = encode_payload("secret_data")  # "c2VjcmV0X2RhdGE"

# --- Handling deep links ---

# Only with payload (F.payload filters out empty starts)
@router.bot_started(F.payload)
async def on_deep_link(event: BotStarted, bot):
    # Raw payload as-is from URL
    raw = event.payload  # "c2VjcmV0X2RhdGE"

    # Decode base64url
    decoded = event.deep_link()  # "secret_data"

    # With custom decryption (e.g. AES)
    # decoded = event.deep_link(decoder=my_cryptor.decrypt)

    await bot.send_message(
        user_id=event.user.user_id,
        text=f"Welcome! Ref: {decoded}",
    )

# Without payload — regular start
@router.bot_started()
async def on_start(event: BotStarted, bot):
    await bot.send_message(
        user_id=event.user.user_id,
        text="Welcome!",
    )
```

### Multiple Routers

```python
from maxgram import Bot, Dispatcher, Router

# Admin router
admin_router = Router(name="admin")


@admin_router.message(Command("ban"))
async def ban_user(message, bot):
    await message.answer(text="User banned.")


# User router
user_router = Router(name="user")


@user_router.message(Command("profile"))
async def show_profile(message, bot):
    await message.answer(text=f"Your ID: {message.sender.user_id}")


# Main setup
dp = Dispatcher()
dp.include_routers(admin_router, user_router)
```

### Startup & Shutdown Events

```python
import logging
from maxgram import Bot, Dispatcher, Router

router = Router()
logger = logging.getLogger(__name__)


@router.startup()
async def on_startup(bot: Bot, dispatcher: Dispatcher):
    me = await bot.get_me()
    logger.info("Bot started: @%s (id=%d)", me.username, me.user_id)


@router.shutdown()
async def on_shutdown(bot: Bot, dispatcher: Dispatcher):
    logger.info("Bot shutting down...")
```

### Error Handling

```python
from maxgram import Router
from maxgram.filters import ExceptionTypeFilter

router = Router()


@router.error(ExceptionTypeFilter(ValueError))
async def handle_value_error(error, bot):
    print(f"ValueError caught: {error}")


@router.error()
async def handle_all_errors(error, bot):
    print(f"Unhandled error: {error}")
```

### Default Bot Properties

```python
from maxgram import Bot
from maxgram.client.default import DefaultBotProperties
from maxgram.enums import ParseMode

# Defaults automatically apply to all send methods
bot = Bot(
    token="YOUR_BOT_TOKEN",
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        disable_link_preview=True,
        notify=False,
    ),
)

# Bot also accepts arbitrary kwargs as attributes
bot = Bot(
    token="YOUR_BOT_TOKEN",
    db=my_database,
    config=my_config,
)
print(bot.db)  # my_database
```

### Debug Mode

```python
# Enable debug logging for incoming updates and outgoing API requests
dp = Dispatcher(
    updates_debug=True,     # Log all incoming updates in readable format
    requests_debug=True,    # Log all outgoing API requests
)
```

### Webhook (aiohttp)

```python
from aiohttp import web
from maxgram import Bot, Dispatcher
from maxgram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()

# ... register handlers ...

app = web.Application()
handler = SimpleRequestHandler(dp, bot, secret_token="your_secret")
handler.register(app, "/webhook")
setup_application(app, dp)
web.run_app(app, host="0.0.0.0", port=8080)
```

### Full Bot Example

```python
import asyncio
import logging

from maxgram import Bot, Dispatcher, F, Router
from maxgram.client.default import DefaultBotProperties
from maxgram.enums import ParseMode
from maxgram.filters import Command, StateFilter, CallbackData
from maxgram.types import BotStarted
from maxgram.fsm.state import State, StatesGroup
from maxgram.fsm.context import FSMContext
from maxgram.utils.keyboard import InlineKeyboardBuilder
from maxgram.utils.formatting import Bold, Text, as_list, as_marked_list

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token="YOUR_BOT_TOKEN",
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()
router = Router()


# --- FSM States ---
class OrderStates(StatesGroup):
    choosing_item = State()
    confirming = State()


# --- Callback Data ---
class ItemCallback(CallbackData, prefix="item"):
    name: str


class ConfirmCallback(CallbackData, prefix="confirm"):
    value: bool


# --- Handlers ---
@router.bot_started()
async def cmd_start(event: BotStarted, bot):
    await bot.send_message(user_id=event.user.user_id, text="Welcome! Use /order to make an order.")


@router.message(Command("order"))
async def cmd_order(message, state: FSMContext, bot):
    builder = InlineKeyboardBuilder()
    builder.callback(text="Pizza", callback_data=ItemCallback(name="pizza"))
    builder.callback(text="Burger", callback_data=ItemCallback(name="burger"))
    builder.adjust(2)

    await state.set_state(OrderStates.choosing_item)
    await message.answer("Choose your item:", keyboard=builder)


@router.message_callback(ItemCallback.filter(), StateFilter(OrderStates.choosing_item))
async def on_item_chosen(callback, callback_data: ItemCallback, state: FSMContext, bot):
    await state.update_data(item=callback_data.name)
    await state.set_state(OrderStates.confirming)

    builder = InlineKeyboardBuilder()
    builder.callback(text="Confirm", callback_data=ConfirmCallback(value=True))
    builder.callback(text="Cancel", callback_data=ConfirmCallback(value=False))
    builder.adjust(2)

    await callback.answer(
        text=f"You chose: {callback_data.name}. Confirm?",
        keyboard=builder,
    )


@router.message_callback(ConfirmCallback.filter(), StateFilter(OrderStates.confirming))
async def on_confirm(callback, callback_data: ConfirmCallback, state: FSMContext, bot):
    if callback_data.value:
        data = await state.get_data()
        content = as_list(
            Bold("Order confirmed!"),
            as_marked_list(f"Item: {data['item']}"),
        )
        await callback.answer(**content.as_kwargs())
    else:
        await callback.answer(text="Order cancelled.")
    await state.clear()


@router.message()
async def echo(message, bot):
    await message.answer(text=message.body.text)


# --- Run ---
dp.include_router(router)
asyncio.run(dp.start_polling(bot))
```

## Links

- MAX Bot API: https://dev.max.ru
- PyPI: https://pypi.org/project/pymaxgram/
