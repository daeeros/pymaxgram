# Прочие утилиты

## Payload

Кодирование/декодирование payload для deep link.

```python
encode_payload(payload: str, encoder: Callable | None = None) -> str
decode_payload(payload: str, decoder: Callable | None = None) -> str
```

По умолчанию используется Base64url. Можно передать кастомные encoder/decoder.

## Token Validation

```python
validate_token(token: str) -> None  # Raises TokenValidationError

class TokenValidationError(Exception): ...
```

## Mixins

### DataMixin

Dict-подобный интерфейс:

```python
class DataMixin:
    __getitem__, __setitem__, __delitem__, __contains__,
    get, setdefault, update
```

### ContextInstanceMixin[T]

Хранение экземпляра через `contextvars`:

```python
class ContextInstanceMixin(Generic[T]):
    @classmethod
    def get_current(cls) -> T | None
    @classmethod
    def set_current(cls, value: T) -> Token
```

## Serialization

```python
deserialize_max_object(obj) -> tuple[dict, list[InputFile]]
deserialize_max_object_to_python(obj) -> dict
```

## MagicFilter

```python
class MagicFilter(magic_filter.MagicFilter):
    def as_(self, name: str) -> ...  # Оборачивает результат с именем
```

Используется для создания глобального `F`:

```python
from maxgram import F

F.body.text.startswith("hello")
```

## Исходные файлы

- `maxgram/utils/payload.py`
- `maxgram/utils/token.py`
- `maxgram/utils/mixins.py`
- `maxgram/utils/serialization.py`
- `maxgram/utils/magic_filter.py`
