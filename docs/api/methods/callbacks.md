# Callbacks

## AnswerCallback

`POST /answers` → `bool`

```python
class AnswerCallback(MaxMethod[bool]):
    callback_id: str
    text: str | None = None
    attachments: list[Any] | None = None
    notification: str | None = None
    notify: bool | None = None
    format: str | None = None
```

- `callback_id` передаётся как query param
- Остальные поля формируют тело запроса в виде `{"message": {...}}`

### Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `callback_id` | `str` | ID callback-запроса (обязательное) |
| `text` | `str \| None` | Текст ответного сообщения |
| `attachments` | `list \| None` | Вложения к ответу |
| `notification` | `str \| None` | Всплывающее уведомление |
| `notify` | `bool \| None` | Отправить push-уведомление |
| `format` | `str \| None` | Формат текста (`"html"` / `"markdown"`) |

## Исходный файл

`maxgram/methods/answer_callback.py`
