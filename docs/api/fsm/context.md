# FSMContext

Контекст FSM для управления состоянием и данными.

```python
class FSMContext:
    def __init__(self, storage: BaseStorage, key: StorageKey) -> None: ...
```

## Методы

| Метод | Описание |
| --- | --- |
| `await set_state(state: str \| State \| None)` | Установить текущее состояние |
| `await get_state() -> str \| None` | Получить текущее состояние |
| `await set_data(data: dict) -> None` | Заменить все данные |
| `await get_data() -> dict` | Получить все данные |
| `await get_value(key, default=None)` | Получить одно значение по ключу |
| `await update_data(**kwargs) -> dict` | Обновить данные (merge) и вернуть результат |
| `await clear() -> None` | Сбросить состояние и данные |

## Использование в обработчике

```python
@router.message()
async def handler(message, state: FSMContext, bot):
    # Установить состояние
    await state.set_state(MyStates.waiting_input)

    # Сохранить данные
    await state.update_data(name="John", age=25)

    # Получить данные
    data = await state.get_data()
    name = await state.get_value("name")

    # Очистить
    await state.clear()
```

## Исходный файл

`maxgram/fsm/context.py`
