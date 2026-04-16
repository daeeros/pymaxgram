# Действия в чате

## SendAction

`POST /chats/{chat_id}/actions` → `bool`

Отправляет индикатор действия в чат.

```python
class SendAction(MaxMethod[bool]):
    chat_id: int
    action: str
```

Доступные значения `action` (`ChatAction`):

| Значение | Описание |
|----------|----------|
| `typing_on` | Бот печатает |
| `sending_photo` | Бот отправляет фото |
| `sending_video` | Бот отправляет видео |
| `sending_audio` | Бот отправляет аудио |
| `sending_file` | Бот отправляет файл |
| `mark_seen` | Бот прочитал сообщения |

## Исходный файл

`maxgram/methods/send_action.py`
