# Прочие фильтры

## ExceptionTypeFilter

Фильтр ошибок по типу исключения.

```python
class ExceptionTypeFilter(Filter):
    def __init__(self, *exception_types: type[Exception]) -> None: ...
```

```python
@router.error(ExceptionTypeFilter(ValueError, TypeError))
async def handle(error, bot): ...
```

## ExceptionMessageFilter

Фильтр ошибок по тексту (regex).

```python
class ExceptionMessageFilter(Filter):
    def __init__(self, pattern: str | re.Pattern) -> None: ...
```

```python
@router.error(ExceptionMessageFilter(r"timeout|connection"))
async def handle(error, bot): ...
```

## MagicData

Фильтр по данным middleware через magic-filter.

```python
class MagicData(Filter):
    def __init__(self, rule: MagicFilter) -> None: ...
```

```python
from maxgram import F
from maxgram.filters import MagicData

@router.message(MagicData(F.event_from_user.is_bot == False))
async def humans_only(message, bot): ...
```

## Логические комбинаторы

```python
def and_f(*filters: Filter) -> _AndFilter
def or_f(*filters: Filter) -> _OrFilter
def invert_f(filter: Filter) -> _InvertFilter
```

- `and_f(A, B)` — все фильтры должны пройти
- `or_f(A, B)` — хотя бы один
- `invert_f(A)` — инверсия (эквивалент `~A`)

```python
from maxgram.filters import or_f, Command

@router.message(or_f(Command("help"), Command("start")))
async def handler(message, bot): ...
```

## Исходные файлы

- `maxgram/filters/exception.py`
- `maxgram/filters/magic_data.py`
- `maxgram/filters/logic.py`
