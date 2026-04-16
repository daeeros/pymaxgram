# Button и InlineKeyboard

## Button

Базовый класс кнопки inline-клавиатуры.

```python
class Button(MaxObject):
    type: str
    text: str
```

Для каждого типа кнопки есть свой подкласс, наследующий `Button`:

| Класс | Поля (помимо `type`, `text`) |
| --- | --- |
| `CallbackButton` | `payload: str \| None` — данные callback |
| `LinkButton` | `url: str` — ссылка (до 2048 символов) |
| `RequestContactButton` | — |
| `RequestGeoLocationButton` | `quick: bool \| None` — отправка без подтверждения |
| `OpenAppButton` | `web_app: str \| None`, `contact_id: int \| None`, `payload: str \| None` |
| `MessageButton` | — |
| `ClipboardButton` | `payload: str` — текст для копирования |

### Пример

```python
from maxgram.types import CallbackButton, LinkButton, ClipboardButton

# Callback-кнопка
btn = CallbackButton(text="Click", payload="data:1")

# Кнопка-ссылка
btn = LinkButton(text="Open", url="https://max.ru")

# Копирование в буфер
btn = ClipboardButton(text="Copy code", payload="PROMO123")
```

## InlineKeyboard

Модель inline-клавиатуры.

```python
class InlineKeyboard(MaxObject):
    buttons: list[list[Button]]
```

Поле `buttons` — двумерный список: внешний список — ряды, внутренний — кнопки в ряду.

### Пример

```python
from maxgram.types import InlineKeyboard, CallbackButton, LinkButton

keyboard = InlineKeyboard(buttons=[
    [
        CallbackButton(text="A", payload="a"),
        CallbackButton(text="B", payload="b"),
    ],
    [
        LinkButton(text="Сайт", url="https://max.ru"),
    ],
])
```

## Исходные файлы

- `maxgram/types/button.py`
- `maxgram/types/inline_keyboard.py`
