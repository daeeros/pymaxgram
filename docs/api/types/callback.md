# Callback

Модель callback от нажатия inline-кнопки.

```python
class Callback(MaxObject):
    callback_id: str
    timestamp: int = 0
    user: User
    payload: str | None = None
    message: Message | None = None
```

!!! note
    `callback.message` автоматически заполняется из Update при парсинге.
    MAX API передаёт message на уровне Update, а не внутри callback —
    pymaxgram пробрасывает его автоматически.

## Поля

| Поле | Тип | Описание |
| --- | --- | --- |
| `callback_id` | `str` | Уникальный ID callback-запроса |
| `timestamp` | `int` | Время нажатия (Unix timestamp) |
| `user` | `User` | Пользователь, нажавший кнопку |
| `payload` | `str \| None` | Данные, переданные в кнопке (payload) |
| `message` | `Message \| None` | Сообщение, к которому прикреплена кнопка |

## Методы

### answer

```python
await callback.answer(
    text: str | None = None,
    attachments: list | None = None,
    notification: str | None = None,
    notify: bool | None = None,
    format: str | None = None,
    keyboard: InlineKeyboardBuilder | InlineKeyboard | list | None = None,
    clear_attachments: bool = True,
) -> bool
```

Отвечает на callback-запрос. Может обновить сообщение и/или показать уведомление.

- **text** — текст для обновления сообщения
- **keyboard** — новая клавиатура
- **notification** — всплывающее уведомление
- **attachments** — вложения
- **notify** — отправить push-уведомление
- **format** — формат текста (`"html"` / `"markdown"`)
- **clear_attachments** — если `True` (по умолчанию), убирает все вложения (включая клавиатуру)
  при отсутствии `keyboard` и `attachments`. Если `False` — вложения сохраняются

```python
# Обновить текст, клавиатура убирается (по умолчанию)
await callback.answer(text="Done!")

# Обновить текст, клавиатура сохраняется
await callback.answer(text="Updated!", clear_attachments=False)

# Обновить текст с новой клавиатурой
await callback.answer(text="Menu:", keyboard=builder)

# Показать всплывающее уведомление (сообщение не меняется)
await callback.answer(notification="Done!")
```

### edit_text

```python
await callback.edit_text(
    text: str | None = None,
    attachments: list | None = None,
    notify: bool | None = None,
    format: str | None = None,
    keyboard: InlineKeyboardBuilder | InlineKeyboard | list | None = None,
    clear_attachments: bool = True,
) -> bool
```

Редактирует сообщение через `PUT /messages`. Требует `callback.message`.
`clear_attachments=True` по умолчанию убирает вложения и клавиатуру.

## Исходный файл

`maxgram/types/callback.py`
