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
   builder.callback(text="Like", payload="vote:like")
   builder.callback(text="Dislike", payload="vote:dislike")
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

Классы кнопок
--------------

Базовый класс ``Button`` содержит только ``type`` и ``text``. Для каждого типа кнопки
есть свой подкласс с нужными полями:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Класс
     - Поля
   * - ``CallbackButton``
     - ``text``, ``payload: str | None``
   * - ``LinkButton``
     - ``text``, ``url: str``
   * - ``RequestContactButton``
     - ``text``
   * - ``RequestGeoLocationButton``
     - ``text``, ``quick: bool | None``
   * - ``OpenAppButton``
     - ``text``, ``web_app: str | None``, ``contact_id: int | None``, ``payload: str | None``
   * - ``MessageButton``
     - ``text``
   * - ``ClipboardButton``
     - ``text``, ``payload: str``

.. code-block:: python

   from maxgram.types import CallbackButton, LinkButton, ClipboardButton

   btn1 = CallbackButton(text="Click", payload="data:1")
   btn2 = LinkButton(text="Open", url="https://max.ru")
   btn3 = ClipboardButton(text="Copy", payload="PROMO123")

InlineKeyboardBuilder
---------------------

Утилита для построения клавиатур:

.. code-block:: python

   from maxgram.utils.keyboard import InlineKeyboardBuilder

   builder = InlineKeyboardBuilder()
   builder.callback(text="Option 1", payload="opt:1")
   builder.callback(text="Option 2", payload="opt:2")
   builder.callback(text="Option 3", payload="opt:3")
   builder.adjust(2)  # 2 кнопки в ряду

   # Отправка
   await message.answer("Choose:", keyboard=builder)

Ограничения:

- Максимум **7** кнопок в ряду
- Максимум **30** рядов
- Максимум **210** кнопок всего

Методы для добавления кнопок:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Метод
     - Описание
   * - ``callback(text, payload?, *, callback_data?)``
     - Callback-кнопка. Отправляет событие ``message_callback``
   * - ``link(text, url)``
     - Открывает ссылку в новой вкладке
   * - ``request_contact(text)``
     - Запрашивает контакт пользователя
   * - ``request_geo_location(text, *, quick?)``
     - Запрашивает геолокацию. ``quick=True`` — без подтверждения
   * - ``open_app(text, *, web_app?, contact_id?, payload?)``
     - Открывает мини-приложение
   * - ``message(text)``
     - Отправляет текст кнопки как сообщение от пользователя
   * - ``clipboard(text, payload)``
     - Копирует ``payload`` в буфер обмена
Методы компоновки:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Метод
     - Описание
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
   builder.callback(text="Buy", callback_data=ItemAction(id=1, action="buy"))
   builder.callback(text="Info", callback_data=ItemAction(id=1, action="info"))

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
   new_builder.callback(text="Done", payload="done")
   await callback.answer(text="Updated!", keyboard=new_builder)
