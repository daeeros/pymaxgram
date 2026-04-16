# Chat

Модель чата MAX.

```python
class Chat(MaxObject):
    chat_id: int
    type: str = "chat"
    status: str = "active"
    title: str | None = None
    icon: Image | None = None
    last_event_time: int = 0
    participants_count: int = 0
    owner_id: int | None = None
    participants: dict[str, Any] | None = None
    is_public: bool = False
    link: str | None = None
    description: str | None = None
    dialog_with_user: UserWithPhoto | None = None
    chat_message_id: str | None = None
    pinned_message: Message | None = None
```

## Поля

| Поле | Тип | Описание |
| --- | --- | --- |
| `chat_id` | `int` | Уникальный ID чата |
| `type` | `str` | Тип чата (`"chat"`, `"dialog"`, `"channel"`) |
| `status` | `str` | Статус (`"active"`, `"removed"`, `"left"`, `"closed"`) |
| `title` | `str \| None` | Название чата |
| `icon` | `Image \| None` | Иконка чата |
| `last_event_time` | `int` | Время последнего события (Unix timestamp) |
| `participants_count` | `int` | Количество участников |
| `owner_id` | `int \| None` | ID владельца |
| `participants` | `dict \| None` | Информация об участниках |
| `is_public` | `bool` | Публичный чат |
| `link` | `str \| None` | Ссылка на чат |
| `description` | `str \| None` | Описание чата |
| `dialog_with_user` | `UserWithPhoto \| None` | Пользователь (для диалогов) |
| `chat_message_id` | `str \| None` | ID сообщения чата |
| `pinned_message` | `Message \| None` | Закреплённое сообщение |

## Image

```python
class Image(MaxObject):
    url: str
    token: str | None = None
    width: int | None = None
    height: int | None = None
```

## Исходные файлы

- `maxgram/types/chat.py`
- `maxgram/types/image.py`
