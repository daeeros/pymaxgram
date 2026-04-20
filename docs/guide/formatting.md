# Форматирование текста

pymaxgram предоставляет несколько способов форматирования текста в сообщениях.

## Режимы разметки

MAX API поддерживает два режима:

- `html` — HTML-разметка
- `markdown` — Markdown-разметка

```python
from maxgram.enums import ParseMode

await message.answer(
    text="<b>Bold</b> and <i>italic</i>",
    format=ParseMode.HTML,
)

await message.answer(
    text="**Bold** and *italic*",
    format=ParseMode.MARKDOWN,
)
```

Можно задать режим по умолчанию через `DefaultBotProperties`. Он будет автоматически
применяться ко всем методам отправки сообщений:

```python
from maxgram import Bot
from maxgram.client.default import DefaultBotProperties
from maxgram.enums import ParseMode

bot = Bot(
    token="TOKEN",
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

# format="html" подставляется автоматически во все вызовы:
# message.answer(), message.reply(), message.edit_text(),
# callback.answer(), bot.send_message(), bot.edit_message()
```

### Поддерживаемые HTML-теги

| Эффект | HTML |
| --- | --- |
| Курсив | `<i>` или `<em>` |
| Жирный | `<b>` или `<strong>` |
| Зачёркнутый | `<del>` или `<s>` |
| Подчёркнутый | `<ins>` или `<u>` |
| Моноширинный | `<pre>` или `<code>` |
| Ссылка | `<a href="url">text</a>` |
| Упоминание | `<a href="max://user/user_id">Имя</a>` |

### Поддерживаемый Markdown

| Эффект | Markdown |
| --- | --- |
| Курсив | `*text*` или `_text_` |
| Жирный | `**text**` или `__text__` |
| Зачёркнутый | `~~text~~` |
| Подчёркнутый | `++text++` |
| Моноширинный | `` `text` `` |
| Ссылка | `[text](url)` |
| Упоминание | `[Имя](max://user/user_id)` |

## Рендеринг входящей разметки

Когда приходит сообщение с `body.markup`, необязательно вручную собирать
HTML из элементов — `MessageBody` имеет готовые свойства:

```python
@router.message()
async def handler(message):
    # Готовый HTML с корректной обработкой UTF-16 оффсетов (эмодзи и др.)
    await message.answer(text=message.body.html_text, format="html")

    # То же самое в Markdown
    await message.answer(text=message.body.md_text, format="markdown")
```

`html_text` экранирует `&`, `<`, `>` в обычных участках текста. Оба свойства
понимают все 7 типов markup-разметки, включая `link` и `user_mention`.

## Утилиты форматирования

Модуль `maxgram.utils.formatting` предоставляет типизированные конструкторы:

```python
from maxgram.utils.formatting import (
    Text, Bold, Italic, Underline, Strikethrough,
    Code, Pre, TextLink, UserMention,
    as_list, as_line, as_marked_list, as_numbered_list,
    as_section, as_key_value,
)
```

### Базовые элементы

```python
Bold("жирный текст")             # <b>жирный текст</b>
Italic("курсив")                 # <i>курсив</i>
Underline("подчёркнутый")        # <u>подчёркнутый</u>
Strikethrough("зачёркнутый")     # <s>зачёркнутый</s>
Code("inline код")               # <code>inline код</code>
Pre("блок кода")                 # <pre>блок кода</pre>
TextLink("ссылка", url="https://max.ru")  # <a href="...">ссылка</a>
UserMention("Иван", user_id=123)          # <a href="max://user/123">Иван</a>
```

### Составные конструкции

```python
# Объединение элементов
text = Text("Привет, ", Bold("мир"), "!")

# Список (каждый элемент на новой строке)
text = as_list(
    "Первая строка",
    Bold("Вторая строка"),
    "Третья строка",
)

# Строка (элементы через пробел)
text = as_line("Имя:", Bold("Иван"))

# Маркированный список
text = as_marked_list(
    "Пункт 1",
    "Пункт 2",
    "Пункт 3",
)

# Нумерованный список
text = as_numbered_list(
    "Первый",
    "Второй",
    "Третий",
)

# Секция с заголовком
text = as_section(
    Bold("Заголовок"),
    as_marked_list("Пункт 1", "Пункт 2"),
)

# Ключ-значение
text = as_key_value("Имя", "Иван")
```

### Отправка

```python
content = as_list(
    Bold("Информация о пользователе"),
    as_marked_list(
        f"Имя: {user.first_name}",
        f"ID: {user.user_id}",
    ),
)

# Автоматически устанавливает text и format
await message.answer(**content.as_kwargs())
```

## Text Decorations

Низкоуровневые функции для прямого форматирования строк:

```python
from maxgram import html, md

# HTML
html.bold("жирный")          # <b>жирный</b>
html.italic("курсив")        # <i>курсив</i>
html.underline("подчёркнутый")  # <u>подчёркнутый</u>
html.strikethrough("зачёркнутый")  # <s>зачёркнутый</s>
html.code("код")             # <code>код</code>
html.link("текст", "https://max.ru")
html.user_mention("Иван", 123)  # <a href="max://user/123">Иван</a>
html.quote("экранирование")  # html.escape()

# Markdown
md.bold("жирный")            # **жирный**
md.italic("курсив")          # *курсив*
md.underline("подчёркнутый") # ++подчёркнутый++
md.strikethrough("зачёркнутый")  # ~~зачёркнутый~~
md.code("код")               # `код`
md.link("текст", "https://max.ru")
md.user_mention("Иван", 123) # [Иван](max://user/123)
```

## Полный пример

```python
from maxgram import Router
from maxgram.filters import Command
from maxgram.utils.formatting import (
    Bold, Code, Pre, Text, UserMention,
    as_list, as_marked_list, as_numbered_list, as_section,
)

router = Router()

@router.message(Command("info"))
async def info(message, bot):
    content = as_list(
        Bold("pymaxgram"),
        "",
        as_section(
            Bold("Возможности"),
            as_numbered_list(
                "Асинхронная архитектура",
                "Типизация через Pydantic",
                "FSM и Middleware",
                "Inline-клавиатуры",
            ),
        ),
        "",
        Text("Установка: ", Code("pip install pymaxgram")),
        "",
        Pre("from maxgram import Bot\nbot = Bot(token='...')"),
    )
    await message.answer(**content.as_kwargs())
```
