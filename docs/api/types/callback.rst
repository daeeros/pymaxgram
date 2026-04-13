==========
Callback
==========

.. module:: maxgram.types.callback

Модель callback от нажатия inline-кнопки.

.. code-block:: python

   class Callback(MaxObject):
       callback_id: str
       timestamp: int = 0
       user: User
       payload: str | None = None
       message: Message | None = None

.. note::

   ``callback.message`` автоматически заполняется из Update при парсинге.
   MAX API передаёт message на уровне Update, а не внутри callback —
   pymaxgram пробрасывает его автоматически.

Поля
----

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Поле
     - Тип
     - Описание
   * - ``callback_id``
     - ``str``
     - Уникальный ID callback-запроса
   * - ``timestamp``
     - ``int``
     - Время нажатия (Unix timestamp)
   * - ``user``
     - ``User``
     - Пользователь, нажавший кнопку
   * - ``payload``
     - ``str | None``
     - Данные, переданные в кнопке (payload)
   * - ``message``
     - ``Message | None``
     - Сообщение, к которому прикреплена кнопка

Методы
------

answer
^^^^^^

.. code-block:: python

   await callback.answer(
       text: str | None = None,
       attachments: list | None = None,
       notification: str | None = None,
       notify: bool | None = None,
       format: str | None = None,
       keyboard: InlineKeyboardBuilder | InlineKeyboard | list | None = None,
   ) -> bool

Отвечает на callback-запрос. Может обновить сообщение и/или показать уведомление.

- **text** — текст для обновления сообщения
- **keyboard** — новая клавиатура
- **notification** — всплывающее уведомление
- **attachments** — вложения
- **notify** — отправить push-уведомление
- **format** — формат текста (``"html"`` / ``"markdown"``)

.. code-block:: python

   # Обновить сообщение с новой клавиатурой
   await callback.answer(text="Updated!", keyboard=builder)

   # Показать всплывающее уведомление
   await callback.answer(notification="Done!")

edit_text
^^^^^^^^^

.. code-block:: python

   await callback.edit_text(
       text: str | None = None,
       attachments: list | None = None,
       notify: bool | None = None,
       format: str | None = None,
       keyboard: InlineKeyboardBuilder | InlineKeyboard | list | None = None,
   ) -> bool

Редактирует сообщение через ``PUT /messages``. Требует ``callback.message``.

delete_message
^^^^^^^^^^^^^^

.. code-block:: python

   await callback.delete_message() -> bool

Удаляет сообщение. Требует ``callback.message``.

Исходный файл
--------------

``maxgram/types/callback.py``
