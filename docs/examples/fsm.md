# FSM (пошаговая регистрация)

```python
import asyncio
from maxgram import Bot, Dispatcher, Router
from maxgram.filters import Command, StateFilter
from maxgram.fsm.state import State, StatesGroup
from maxgram.fsm.context import FSMContext

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()
router = Router()

class RegistrationStates(StatesGroup):
    waiting_name = State()
    waiting_age = State()
    waiting_confirm = State()

@router.message(Command("register"))
async def start_registration(message, state: FSMContext, bot):
    await state.set_state(RegistrationStates.waiting_name)
    await message.answer(text="What is your name?")

@router.message(Command("cancel"))
async def cancel(message, state: FSMContext, bot):
    current = await state.get_state()
    if current is None:
        await message.answer(text="Nothing to cancel.")
        return
    await state.clear()
    await message.answer(text="Registration cancelled.")

@router.message(StateFilter(RegistrationStates.waiting_name))
async def process_name(message, state: FSMContext, bot):
    name = message.body.text
    if len(name) < 2:
        await message.answer(text="Name too short. Try again:")
        return
    await state.update_data(name=name)
    await state.set_state(RegistrationStates.waiting_age)
    await message.answer(text=f"Nice, {name}! How old are you?")

@router.message(StateFilter(RegistrationStates.waiting_age))
async def process_age(message, state: FSMContext, bot):
    try:
        age = int(message.body.text)
    except ValueError:
        await message.answer(text="Please enter a valid number.")
        return

    if age < 1 or age > 150:
        await message.answer(text="Invalid age. Try again:")
        return

    await state.update_data(age=age)
    data = await state.get_data()
    await state.clear()
    await message.answer(
        text=f"Registration complete!\n"
        f"Name: {data['name']}\n"
        f"Age: {age}"
    )

@router.message()
async def echo(message, bot):
    await message.answer(text="Send /register to start or /cancel to abort.")

dp.include_router(router)
asyncio.run(dp.start_polling(bot))
```
