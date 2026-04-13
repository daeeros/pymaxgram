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

Методы
------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Метод
     - Описание
   * - ``button(text, type?, payload?, url?, callback_data?)``
     - Добавить кнопку
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
   builder.button(text="1", payload="n:1")
   builder.button(text="2", payload="n:2")
   builder.button(text="3", payload="n:3")
   builder.button(text="4", payload="n:4")
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
