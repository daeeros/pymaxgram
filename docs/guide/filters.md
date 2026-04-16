# Фильтры

Фильтры определяют, какие события будет обрабатывать конкретный обработчик.

## Базовый принцип

Фильтры передаются как аргументы декоратора:

```python
@router.message(Filter1(), Filter2(), ...)
async def handler(message, bot):
    pass
```

Все фильтры должны вернуть `True` (или `dict`) — работает как логическое И.

## MagicFilter (F)

Объект `F` — декларативный фильтр на основе `magic-filter`:

```python
from maxgram import F

# Точное совпадение текста
@router.message(F.body.text == "hello")

# Проверка начала строки
@router.message(F.body.text.startswith("/"))

# Проверка отправителя
@router.message(F.sender.is_bot == False)

# Callback payload
@router.message_callback(F.payload == "action:like")
@router.message_callback(F.payload.startswith("vote:"))

# Проверка наличия поля
@router.message(F.body.attachments)
```

## Command

Фильтр для текстовых команд (сообщения, начинающиеся с `/`):

```python
from maxgram.filters import Command, CommandObject

@router.message(Command("help"))
async def help_handler(message, bot):
    pass

@router.message(Command("echo"))
async def echo_handler(message, command: CommandObject, bot):
    print(command.command)  # "echo"
    print(command.args)     # текст после команды
    print(command.prefix)   # "/"
```

Параметры `Command`:

| Параметр | Тип | Описание |
| --- | --- | --- |
| `commands` | `str \| list[str]` | Имена команд (без `/`) |
| `prefix` | `str` | Префикс команды (по умолчанию `"/"`) |
| `ignore_case` | `bool` | Игнорировать регистр (`False`) |
| `ignore_mention` | `bool` | Игнорировать упоминание бота (`False`) |
| `magic` | `MagicFilter \| None` | Дополнительный фильтр magic-filter |

### CommandObject

Результат парсинга команды, инъектируется в обработчик:

| Поле | Тип | Описание |
| --- | --- | --- |
| `prefix` | `str` | Префикс (`"/"`) |
| `command` | `str` | Имя команды (`"help"`) |
| `mention` | `str \| None` | Упоминание бота |
| `args` | `str \| None` | Аргументы после команды |
| `regexp_match` | `re.Match \| None` | Результат регулярного выражения |
| `magic_result` | `Any` | Результат magic-filter |

## CallbackData

Структурированные callback-данные на основе Pydantic:

```python
from maxgram.filters import CallbackData

class ProductAction(CallbackData, prefix="product"):
    id: int
    action: str

# Упаковка (при создании кнопки)
payload = ProductAction(id=42, action="buy").pack()
# Результат: "product:42:buy"

# Фильтр
@router.message_callback(ProductAction.filter())
async def on_product(callback, callback_data: ProductAction, bot):
    print(callback_data.id)      # 42
    print(callback_data.action)  # "buy"
```

!!! warning

    Максимальная длина payload — **128 байт**. Учитывайте это при проектировании
    структуры CallbackData.

Поддерживаемые типы полей:

- `str`, `int`, `float`
- `bool`
- `Enum`
- `UUID`
- `Decimal`, `Fraction`

## StateFilter

Фильтр по текущему состоянию FSM:

```python
from maxgram.filters import StateFilter
from maxgram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    age = State()

@router.message(StateFilter(Form.name))
async def get_name(message, state, bot):
    pass

# Любое состояние
@router.message(StateFilter("*"))
async def any_state(message, bot):
    pass

# Без состояния (по умолчанию)
@router.message(StateFilter(None))
async def no_state(message, bot):
    pass
```

## ExceptionTypeFilter

Фильтр ошибок по типу исключения:

```python
from maxgram.filters import ExceptionTypeFilter

@router.error(ExceptionTypeFilter(ValueError))
async def handle_value_error(error, bot):
    pass
```

## ExceptionMessageFilter

Фильтр ошибок по тексту сообщения (regex):

```python
from maxgram.filters import ExceptionMessageFilter

@router.error(ExceptionMessageFilter(r"timeout"))
async def handle_timeout(error, bot):
    pass
```

## MagicData

Фильтр по данным middleware:

```python
from maxgram.filters import MagicData

@router.message(MagicData(F.event_from_user.is_bot == False))
async def humans_only(message, bot):
    pass
```

## Логические комбинаторы

```python
from maxgram.filters import and_f, or_f, invert_f

# ИЛИ
@router.message(or_f(Command("help"), Command("start")))

# И
@router.message(and_f(Filter1(), Filter2()))

# НЕ (инверсия)
@router.message(invert_f(Command("admin")))

# Через оператор ~
@router.message(~Command("admin"))
```

## Пользовательские фильтры

```python
from maxgram.filters import Filter

class IsAdmin(Filter):
    def __init__(self, admin_ids: set[int]):
        self.admin_ids = admin_ids

    async def __call__(self, message, **kwargs) -> bool:
        if message.sender:
            return message.sender.user_id in self.admin_ids
        return False

# Использование
@router.message(IsAdmin({123, 456}), Command("ban"))
async def ban(message, bot):
    pass
```

Фильтр может возвращать `dict` для передачи данных в обработчик:

```python
class ExtractUser(Filter):
    async def __call__(self, message, **kwargs) -> dict | bool:
        if message.sender:
            return {"user_name": message.sender.first_name}
        return False

@router.message(ExtractUser())
async def handler(message, user_name: str, bot):
    await message.answer(text=f"Hello, {user_name}!")
```
