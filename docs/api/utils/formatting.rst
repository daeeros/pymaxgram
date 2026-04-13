===============
Форматирование
===============

Text Decorations
----------------

.. module:: maxgram.utils.text_decorations

.. code-block:: python

   from maxgram import html, md

   # HTML-декорации
   html.bold("text")              # <b>text</b>
   html.italic("text")            # <i>text</i>
   html.underline("text")         # <u>text</u>
   html.strikethrough("text")     # <s>text</s>
   html.code("text")              # <code>text</code>
   html.link("text", "url")       # <a href="url">text</a>
   html.user_mention("Name", 123) # <a href="max://user/123">Name</a>
   html.quote("text")             # html.escape()

   # Markdown-декорации
   md.bold("text")                # **text**
   md.italic("text")              # *text*
   md.underline("text")           # ++text++
   md.strikethrough("text")       # ~~text~~
   md.code("text")                # `text`
   md.link("text", "url")         # [text](url)
   md.user_mention("Name", 123)   # [Name](max://user/123)

Formatting Elements
-------------------

.. module:: maxgram.utils.formatting

Типизированные элементы форматирования:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Класс
     - Описание
   * - ``Text(*parts)``
     - Базовый текстовый элемент
   * - ``Bold(*parts)``
     - Жирный: ``<b>``
   * - ``Italic(*parts)``
     - Курсив: ``<i>``
   * - ``Underline(*parts)``
     - Подчёркнутый: ``<u>``
   * - ``Strikethrough(*parts)``
     - Зачёркнутый: ``<s>``
   * - ``Code(text)``
     - Inline-код: ``<code>``
   * - ``Pre(text)``
     - Блок кода: ``<pre>``
   * - ``TextLink(text, url=...)``
     - Гиперссылка: ``<a href="...">``
   * - ``UserMention(text, user_id=...)``
     - Упоминание: ``<a href="max://user/...">``

Функции-утилиты
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Функция
     - Описание
   * - ``as_list(*items, sep="\\n")``
     - Элементы через разделитель
   * - ``as_line(*items, sep=" ")``
     - Элементы через пробел
   * - ``as_marked_list(*items, marker="- ")``
     - Маркированный список
   * - ``as_numbered_list(*items)``
     - Нумерованный список
   * - ``as_section(title, *body)``
     - Секция с заголовком
   * - ``as_key_value(key, value)``
     - Пара ключ-значение

Методы ``Text``:

- ``as_kwargs() -> dict`` — ``{"text": ..., "format": "html"}`` для ``message.answer()``
- ``as_caption_kwargs() -> dict`` — для caption

Исходные файлы
--------------

- ``maxgram/utils/text_decorations.py``
- ``maxgram/utils/formatting.py``
