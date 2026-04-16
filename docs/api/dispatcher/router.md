# Router

Маршрутизатор событий.

```python
class Router:
    def __init__(self, *, name: str | None = None) -> None: ...
```

## Атрибуты

| Атрибут | Тип | Описание |
| --- | --- | --- |
| `name` | `str` | Имя роутера (по умолчанию `hex(id(self))`) |
| `message` | `MaxEventObserver` | `message_created` — новые сообщения |
| `message_callback` | `MaxEventObserver` | `message_callback` — нажатия inline-кнопок |
| `message_edited` | `MaxEventObserver` | `message_edited` — редактирование сообщений |
| `message_removed` | `MaxEventObserver` | `message_removed` — удаление сообщений |
| `bot_started` | `MaxEventObserver` | `bot_started` — запуск бота |
| `bot_stopped` | `MaxEventObserver` | `bot_stopped` — остановка бота |
| `bot_added` | `MaxEventObserver` | `bot_added` — бот добавлен в чат |
| `bot_removed` | `MaxEventObserver` | `bot_removed` — бот удалён из чата |
| `user_added` | `MaxEventObserver` | `user_added` — пользователь добавлен |
| `user_removed` | `MaxEventObserver` | `user_removed` — пользователь удалён |
| `chat_title_changed` | `MaxEventObserver` | `chat_title_changed` — название чата изменено |
| `dialog_muted` | `MaxEventObserver` | `dialog_muted` — уведомления отключены |
| `dialog_unmuted` | `MaxEventObserver` | `dialog_unmuted` — уведомления включены |
| `dialog_cleared` | `MaxEventObserver` | `dialog_cleared` — диалог очищен |
| `dialog_removed` | `MaxEventObserver` | `dialog_removed` — диалог удалён |
| `error` / `errors` | `MaxEventObserver` | Ошибки обработки |
| `startup` | `EventObserver` | Событие запуска |
| `shutdown` | `EventObserver` | Событие остановки |
| `sub_routers` | `list[Router]` | Дочерние роутеры |
| `observers` | `dict[str, MaxEventObserver]` | Словарь наблюдателей по именам |

## Методы

### include_router

```python
def include_router(self, router: Router) -> Router
```

Подключает дочерний роутер. Устанавливает `parent_router`.

### include_routers

```python
def include_routers(self, *routers: Router) -> None
```

Подключает несколько дочерних роутеров.

### propagate_event

```python
async def propagate_event(
    self,
    update_type: str,
    event: MaxObject,
    **kwargs,
) -> Any
```

Передаёт событие по дереву роутеров. Возвращает результат обработчика или `UNHANDLED`.

### resolve_used_update_types

```python
def resolve_used_update_types(
    self,
    skip_events: set[str] | None = None,
) -> list[str]
```

Определяет типы обновлений, для которых зарегистрированы обработчики.

### emit_startup / emit_shutdown

```python
async def emit_startup(self, *args, **kwargs) -> None
async def emit_shutdown(self, *args, **kwargs) -> None
```

Вызывает события жизненного цикла рекурсивно по дереву роутеров.

## Свойства

- `parent_router` → `Router | None` — родительский роутер
- `chain_head` → генератор от текущего к корню
- `chain_tail` → генератор от текущего ко всем потомкам

## Константы

```python
INTERNAL_UPDATE_TYPES: frozenset[str] = frozenset({"update", "error"})
```

## Исходный файл

`maxgram/dispatcher/router.py`
