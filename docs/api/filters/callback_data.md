# CallbackData

Структурированные callback-данные на основе Pydantic.

## CallbackData

```python
class CallbackData(BaseModel):
    """
    Подкласс для определения структуры callback payload.
    Наследуйте и укажите prefix.
    """

    class Config:
        # Автоматически задаётся через __init_subclass__
        ...

    __separator__: ClassVar[str] = ":"
    __prefix__: ClassVar[str]
```

### Создание

```python
class MyCallback(CallbackData, prefix="my"):
    id: int
    action: str

# Упаковка
payload = MyCallback(id=42, action="buy").pack()
# Результат: "my:42:buy"

# Распаковка
data = MyCallback.unpack("my:42:buy")
# data.id == 42, data.action == "buy"
```

### Методы класса

| Метод | Описание |
| --- | --- |
| `pack() -> str` | Сериализует в строку `prefix:field1:field2:...` |
| `unpack(value: str) -> Self` | Десериализует из строки |
| `filter(*rules) -> CallbackDataFilter` | Создаёт фильтр для роутера |

Поддерживаемые типы полей:

- `str`, `int`, `float`, `bool`
- `Enum`
- `UUID`
- `Decimal`, `Fraction`
- `Optional[T]`

!!! warning

    Максимальная длина payload: **128 байт** (`MAX_CALLBACK_LENGTH`).

## CallbackDataFilter

```python
class CallbackDataFilter(Filter):
    callback_data: type[CallbackData]
    rule: MagicFilter | None
```

При совпадении инъектирует `callback_data: MyCallback` в обработчик.

## Пример

```python
class Vote(CallbackData, prefix="vote"):
    item_id: int
    value: bool

@router.message_callback(Vote.filter())
async def on_vote(callback, callback_data: Vote, bot):
    if callback_data.value:
        await callback.answer(notification=f"Liked #{callback_data.item_id}")

# С дополнительным фильтром
@router.message_callback(Vote.filter(F.value == True))
async def on_like_only(callback, callback_data: Vote, bot):
    pass
```

## Исходный файл

`maxgram/filters/callback_data.py`
