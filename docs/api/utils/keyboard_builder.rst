=======================
InlineKeyboardBuilder
=======================

.. module:: maxgram.utils.keyboard

Утилита для построения inline-клавиатур.

.. code-block:: python

   class InlineKeyboardBuilder:
       MAX_WIDTH = 7        # Макс. кнопок в ряду
       MAX_ROWS = 30        # Макс. рядов
       MAX_BUTTONS = 210    # Макс. кнопок всего

Методы для добавления кнопок
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

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
   * - ``button(text, type?, payload?, url?, callback_data?)``
     - Универсальный метод (для обратной совместимости)

Методы компоновки
------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Метод
     - Описание
   * - ``row(*buttons)``
     - Начать новый ряд
   * - ``adjust(*sizes: int)``
     - Перераспределить кнопки: ``adjust(2, 1)`` → 2 кнопки в 1-м ряду, 1 во 2-м
   * - ``copy()``
     - Создать копию builder
   * - ``export() -> list[list[Button]]``
     - Получить список рядов кнопок
   * - ``as_markup() -> InlineKeyboardAttachmentRequest``
     - Получить объект вложения для API

Пример
------

.. code-block:: python

   from maxgram.utils.keyboard import InlineKeyboardBuilder

   builder = InlineKeyboardBuilder()
   builder.callback(text="1", payload="n:1")
   builder.callback(text="2", payload="n:2")
   builder.link(text="Website", url="https://max.ru")
   builder.clipboard(text="Copy code", payload="PROMO123")
   builder.adjust(2)  # 2 кнопки в ряду

   # Отправка через keyboard=
   await message.answer("Choose:", keyboard=builder)

prepare_keyboard
----------------

.. code-block:: python

   from maxgram.utils.keyboard import prepare_keyboard

   def prepare_keyboard(
       attachments: list[Any] | None,
       keyboard: InlineKeyboardBuilder | InlineKeyboard | list[list[Button]] | None,
   ) -> list[Any] | None

Хелпер для конвертации ``keyboard`` в формат ``attachments``. Используется
внутри ``message.answer(keyboard=...)``, ``bot.send_message(keyboard=...)`` и т.д.

Исходный файл
--------------

``maxgram/utils/keyboard.py``
