# Система событий

## EventObserver

Простой наблюдатель для событий жизненного цикла (startup/shutdown).

```python
class EventObserver:
    handlers: list[HandlerObject]

    def register(self, callback, *args, **kwargs) -> None
    async def trigger(self, *args, **kwargs) -> None
    def __call__(self) -> decorator  # Регистрация через декоратор
```

## MaxEventObserver

Наблюдатель для MAX-событий с поддержкой фильтров и middleware.

```python
class MaxEventObserver:
    handlers: list[HandlerObject]
    filters: list[Any]

    def register(self, callback, *filters, **kwargs) -> HandlerObject
    def filter(self, *filters) -> None  # Root-фильтры
    async def trigger(self, event, **kwargs) -> Any
    def middleware(self, middleware) -> None  # Inner middleware
    def outer_middleware(self, middleware) -> None  # Outer middleware
    async def wrap_outer_middleware(self, callback, event, data) -> Any
    async def check_root_filters(self, event, **kwargs) -> tuple[bool, dict]
```

Возвращаемые значения `trigger()`:

- Результат обработчика — если нашёлся совпадающий
- `REJECTED` — если ни один обработчик не совпал
- `UNHANDLED` — если нет обработчиков

## HandlerObject

Обёртка зарегистрированного обработчика.

```python
class HandlerObject:
    callback: Any           # Функция/класс обработчика
    filters: list[FilterObject]

    async def check(self, event, **kwargs) -> tuple[bool, dict]
    def call(self, event, **kwargs) -> Any
```

## FilterObject

Обёртка для фильтра.

```python
class FilterObject:
    callback: Any

    async def call(self, event, **kwargs) -> bool | dict
```

## CallableObject

Базовый класс для интроспекции вызываемых объектов:

- Определяет сигнатуру (params, varkw)
- Различает sync/async
- Подготавливает kwargs для вызова

## Sentinel-значения

```python
UNHANDLED = sentinel.UNHANDLED  # Событие не обработано
REJECTED = sentinel.REJECTED    # Ни один обработчик не совпал
```

## Исключения управления потоком

```python
class SkipHandler(Exception): ...    # Пропустить текущий обработчик
class CancelHandler(Exception): ...  # Отменить всю обработку
```

## Исходные файлы

- `maxgram/dispatcher/event/event.py`
- `maxgram/dispatcher/event/max.py`
- `maxgram/dispatcher/event/handler.py`
- `maxgram/dispatcher/event/bases.py`
