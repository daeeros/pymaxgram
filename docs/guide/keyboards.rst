===========
Клавиатуры
===========

pymaxgram поддерживает inline-клавиатуры для интерактивных сообщений.

Быстрый способ (keyboard=)
---------------------------

Самый удобный способ — использовать параметр ``keyboard=`` при отправке сообщений:

.. code-block:: python

   from maxgram.utils.keyboard import InlineKeyboardBuilder

   builder = InlineKeyboardBuilder()
   builder.button(text="Like", payload="vote:like")
   builder.button(text="Dislike", payload="vote:dislike")
   builder.adjust(2)  # 2 кнопки в ряду

   await message.answer("Rate our bot:", keyboard=builder)

Параметр ``keyboard=`` поддерживается во всех методах отправки:

- ``message.answer(keyboard=...)``
- ``message.reply(keyboard=...)``
- ``message.edit_text(keyboard=...)``
- ``callback.answer(keyboard=...)``
- ``bot.send_message(keyboard=...)``
- ``bot.edit_message(keyboard=...)``
- ``bot.answer_callback(keyboard=...)``

Принимает:

- ``InlineKeyboardBuilder`` — результат builder
- ``InlineKeyboard`` — объект клавиатуры
- ``list[list[Button]]`` — двумерный список кнопок

.. note::

   ``keyboard=`` можно комбинировать с ``attachments=`` — клавиатура будет
   добавлена к остальным вложениям.

Типы кнопок (ButtonType)
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Тип
     - Описание
   * - ``CALLBACK``
     - Отправляет callback с payload. Обрабатывается через ``router.message_callback()``
   * - ``LINK``
     - Открывает URL в браузере. Требует ``url``
   * - ``REQUEST_CONTACT``
     - Запрашивает контакт пользователя
   * - ``REQUEST_GEO_LOCATION``
     - Запрашивает геолокацию
   * - ``OPEN_APP``
     - Открывает приложение
   * - ``MESSAGE``
     - Отправляет сообщение
   * - ``CLIPBOARD``
     - Копирует текст в буфер обмена

Модель Button
-------------

.. code-block:: python

   Button(
       type: str,                  # Тип кнопки (ButtonType)
       text: str,                  # Текст на кнопке
       payload: str | None = None, # Данные для CALLBACK / CLIPBOARD
       url: str | None = None,     # URL для LINK
       intent: str | None = None,  # Намерение
   )

InlineKeyboardBuilder
---------------------

Утилита для построения клавиатур:

.. code-block:: python

   from maxgram.utils.keyboard import InlineKeyboardBuilder

   builder = InlineKeyboardBuilder()
   builder.button(text="Option 1", payload="opt:1")
   builder.button(text="Option 2", payload="opt:2")
   builder.button(text="Option 3", payload="opt:3")
   builder.adjust(2)  # 2 кнопки в ряду

   # Отправка
   await message.answer("Choose:", keyboard=builder)

Ограничения:

- Максимум **7** кнопок в ряду
- Максимум **30** рядов
- Максимум **210** кнопок всего

Методы builder:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Метод
     - Описание
   * - ``button(text, type?, payload?, url?, callback_data?)``
     - Добавить кнопку
   * - ``row(*buttons)``
     - Начать новый ряд
   * - ``adjust(*sizes)``
     - Перераспределить кнопки по рядам
   * - ``copy()``
     - Создать копию builder
   * - ``export()``
     - Получить ``list[list[Button]]``
   * - ``as_markup()``
     - Получить ``InlineKeyboardAttachmentRequest``

CallbackData с клавиатурами
----------------------------

.. code-block:: python

   from maxgram.filters import CallbackData
   from maxgram.utils.keyboard import InlineKeyboardBuilder

   class ItemAction(CallbackData, prefix="item"):
       id: int
       action: str

   builder = InlineKeyboardBuilder()
   builder.button(text="Buy", callback_data=ItemAction(id=1, action="buy"))
   builder.button(text="Info", callback_data=ItemAction(id=1, action="info"))

   await message.answer("Products:", keyboard=builder)

   # Обработка
   @router.message_callback(ItemAction.filter())
   async def on_item(callback, callback_data: ItemAction, bot):
       await callback.answer(
           notification=f"Item #{callback_data.id}: {callback_data.action}"
       )

Обработка callback
------------------

.. code-block:: python

   from maxgram import F

   # По точному payload
   @router.message_callback(F.payload == "action:like")
   async def on_like(callback, bot):
       await callback.answer(notification="Thanks!")

   # По префиксу
   @router.message_callback(F.payload.startswith("vote:"))
   async def on_vote(callback, bot):
       action = callback.payload.split(":")[1]
       await callback.answer(notification=f"Voted: {action}")

Ответ на callback с клавиатурой
--------------------------------

.. code-block:: python

   # Уведомление (всплывающее)
   await callback.answer(notification="Success!")

   # Обновить сообщение с новой клавиатурой
   new_builder = InlineKeyboardBuilder()
   new_builder.button(text="Done", payload="done")
   await callback.answer(text="Updated!", keyboard=new_builder)
