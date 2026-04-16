# StateFilter

Фильтр по текущему FSM-состоянию.

```python
class StateFilter(Filter):
    def __init__(
        self,
        *states: str | State | StatesGroup | type[StatesGroup] | None,
    ) -> None: ...
```

Принимает одно или несколько состояний для проверки.

## Варианты использования

```python
from maxgram.filters import StateFilter
from maxgram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    age = State()

# Конкретное состояние
@router.message(StateFilter(Form.name))

# Несколько состояний
@router.message(StateFilter(Form.name, Form.age))

# Вся группа (любое состояние из группы)
@router.message(StateFilter(Form))

# Любое состояние (не None)
@router.message(StateFilter("*"))

# Без состояния (по умолчанию)
@router.message(StateFilter(None))
```

Использует `raw_state` из данных middleware для сравнения.

## Исходный файл

`maxgram/filters/state.py`
