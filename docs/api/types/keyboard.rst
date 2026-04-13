============================
Button и InlineKeyboard
============================

Button
------

.. module:: maxgram.types.button

Модель кнопки inline-клавиатуры.

.. code-block:: python

   class Button(MaxObject):
       type: str
       text: str
       payload: str | None = None
       url: str | None = None
       intent: str | None = None

Поля
^^^^

.. list-table::
   :header-rows: 1
   :widths: 15 20 65

   * - Поле
     - Тип
     - Описание
   * - ``type``
     - ``str``
     - Тип кнопки (``ButtonType``)
   * - ``text``
     - ``str``
     - Текст на кнопке
   * - ``payload``
     - ``str | None``
     - Данные callback (для ``CALLBACK``)
   * - ``url``
     - ``str | None``
     - URL (для ``LINK``)
   * - ``intent``
     - ``str | None``
     - Намерение

Пример
^^^^^^

.. code-block:: python

   from maxgram.types import Button
   from maxgram.enums import ButtonType

   # Callback-кнопка
   btn = Button(type=ButtonType.CALLBACK, text="Click", payload="data:1")

   # Кнопка-ссылка
   btn = Button(type=ButtonType.LINK, text="Open", url="https://max.ru")

InlineKeyboard
--------------

.. module:: maxgram.types.inline_keyboard

Модель inline-клавиатуры.

.. code-block:: python

   class InlineKeyboard(MaxObject):
       buttons: list[list[Button]]

Поле ``buttons`` — двумерный список: внешний список — ряды, внутренний — кнопки в ряду.

Пример
^^^^^^

.. code-block:: python

   from maxgram.types import InlineKeyboard, Button
   from maxgram.enums import ButtonType

   keyboard = InlineKeyboard(buttons=[
       [
           Button(type=ButtonType.CALLBACK, text="A", payload="a"),
           Button(type=ButtonType.CALLBACK, text="B", payload="b"),
       ],
       [
           Button(type=ButtonType.LINK, text="Сайт", url="https://max.ru"),
       ],
   ])

Исходные файлы
--------------

- ``maxgram/types/button.py``
- ``maxgram/types/inline_keyboard.py``
