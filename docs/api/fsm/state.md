# State и StatesGroup

## State

Одно состояние FSM.

```python
class State:
    # Автоматически получает имя через __set_name__
    # Строковое представление: "GroupName:state_name"

    def __call__(self, ...) -> StateFilter  # Создаёт фильтр
```

## StatesGroup

Группа состояний. Использует метакласс `StatesGroupMeta`.

```python
class StatesGroupMeta(type):
    """Метакласс для регистрации State-атрибутов."""
    __states__: tuple[State, ...]
    __childs__: tuple[StatesGroup, ...]
    __all_states__: tuple[State, ...]
    __all_states_names__: tuple[str, ...]

class StatesGroup(metaclass=StatesGroupMeta):
    pass
```

### Определение состояний

```python
class Form(StatesGroup):
    name = State()
    age = State()

# Вложенные группы
class Main(StatesGroup):
    idle = State()

    class Registration(StatesGroup):
        name = State()
        age = State()
```

Атрибуты `StatesGroup`:

- `Form.__states__` → `(Form.name, Form.age)`
- `Form.__all_states__` → все состояния включая вложенные
- `Form.__all_states_names__` → `("Form:name", "Form:age")`

### Специальные состояния

- `State.default_state` — состояние по умолчанию (`None`)
- `State.any_state` — любое состояние (`"*"`)

## Исходный файл

`maxgram/fsm/state.py`
