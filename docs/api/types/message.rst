=========
Message
=========

.. module:: maxgram.types.message

Модель сообщения MAX.

Message
-------

.. code-block:: python

   class Message(MaxObject):
       sender: User | None = None
       recipient: Recipient
       timestamp: int = 0
       link: LinkedMessage | None = None
       body: MessageBody
       stat: MessageStat | None = None
       url: str | None = None

Поля
^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Поле
     - Тип
     - Описание
   * - ``sender``
     - ``User | None``
     - Отправитель сообщения
   * - ``recipient``
     - ``Recipient``
     - Получатель (чат или пользователь)
   * - ``timestamp``
     - ``int``
     - Время отправки (Unix timestamp)
   * - ``link``
     - ``LinkedMessage | None``
     - Ссылка на другое сообщение (ответ/пересылка)
   * - ``body``
     - ``MessageBody``
     - Тело сообщения (текст + вложения)
   * - ``stat``
     - ``MessageStat | None``
     - Статистика (просмотры для каналов)
   * - ``url``
     - ``str | None``
     - URL сообщения

Методы
^^^^^^

.. code-block:: python

   # Ответить в тот же чат
   await message.answer(
       text: str | None = None,
       attachments: list | None = None,
       notify: bool | None = None,
       format: str | None = None,
       disable_link_preview: bool | None = None,
       keyboard: InlineKeyboardBuilder | InlineKeyboard | list | None = None,
   ) -> Message

   # Ответить с цитированием
   await message.reply(
       text: str | None = None,
       attachments: list | None = None,
       notify: bool | None = None,
       format: str | None = None,
       disable_link_preview: bool | None = None,
       keyboard: InlineKeyboardBuilder | InlineKeyboard | list | None = None,
   ) -> Message

   # Удалить сообщение
   await message.delete() -> bool

   # Отредактировать текст
   await message.edit_text(
       text: str | None = None,
       attachments: list | None = None,
       notify: bool | None = None,
       format: str | None = None,
       keyboard: InlineKeyboardBuilder | InlineKeyboard | list | None = None,
   ) -> bool

MessageBody
-----------

.. module:: maxgram.types.message_body

.. code-block:: python

   class MessageBody(MaxObject):
       mid: str                                      # ID сообщения
       seq: int = 0                                  # Порядковый номер
       text: str | None = None                       # Текст
       attachments: list[Attachment] | None = None    # Вложения
       markup: list[MarkupElement] | None = None      # Разметка текста

MarkupElement
^^^^^^^^^^^^^

.. module:: maxgram.types.markup

Элемент разметки текста. MAX API возвращает разметку в виде массива элементов
с позицией и длиной.

.. code-block:: python

   from pydantic import Field

   class MarkupElement(MaxObject):
       type: str                          # Тип разметки
       from_pos: int = Field(alias="from")  # Начало в тексте (0-based)
       length: int                        # Длина
       url: str | None = None             # Только для link
       user_link: str | None = None       # Только для user_mention (@username)
       user_id: int | None = None         # Только для user_mention (ID)

Типы разметки (``MarkupType``):

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Тип
     - Enum
     - Описание
   * - ``strong``
     - ``MarkupType.STRONG``
     - Жирный
   * - ``emphasized``
     - ``MarkupType.EMPHASIZED``
     - Курсив
   * - ``monospaced``
     - ``MarkupType.MONOSPACED``
     - Моноширинный
   * - ``link``
     - ``MarkupType.LINK``
     - Ссылка (+ поле ``url``)
   * - ``strikethrough``
     - ``MarkupType.STRIKETHROUGH``
     - Зачёркнутый
   * - ``underline``
     - ``MarkupType.UNDERLINE``
     - Подчёркнутый
   * - ``user_mention``
     - ``MarkupType.USER_MENTION``
     - Упоминание (+ ``user_id``, ``user_link``)

Пример:

.. code-block:: python

   @router.message()
   async def handler(message: Message, bot):
       if message.body.markup:
           for el in message.body.markup:
               print(f"{el.type}: pos={el.from_pos}, len={el.length}")
               if el.type == "link":
                   print(f"  url: {el.url}")
               if el.type == "user_mention":
                   print(f"  user: {el.user_id} ({el.user_link})")

MessageStat
-----------

.. module:: maxgram.types.message_stat

.. code-block:: python

   class MessageStat(MaxObject):
       views: int | None = None  # Количество просмотров

LinkedMessage
-------------

.. module:: maxgram.types.linked_message

Ссылка на другое сообщение (ответ или пересылка).

.. code-block:: python

   class LinkedMessage(MaxObject):
       type: str                      # "forward" или "reply"
       sender: User | None = None     # Автор оригинала
       chat_id: int | None = None     # Чат оригинала
       message: MessageBody | None = None  # Тело оригинала

Recipient
---------

.. module:: maxgram.types.recipient

.. code-block:: python

   class Recipient(MaxObject):
       chat_id: int | None = None     # ID чата
       chat_type: str | None = None   # Тип чата
       user_id: int | None = None     # ID пользователя (для ЛС)

NewMessageBody
--------------

.. module:: maxgram.types.new_message_body

Тело для создания/редактирования сообщений.

.. code-block:: python

   class NewMessageBody(MaxObject):
       text: str | None = None
       attachments: list[AttachmentRequest] | None = None
       link: NewMessageLink | None = None
       notify: bool | None = None
       format: str | None = None      # "html" или "markdown"

NewMessageLink
--------------

.. module:: maxgram.types.new_message_link

.. code-block:: python

   class NewMessageLink(MaxObject):
       type: str   # "reply" или "forward"
       mid: str    # ID сообщения

Исходные файлы
--------------

- ``maxgram/types/message.py``
- ``maxgram/types/message_body.py``
- ``maxgram/types/markup.py``
- ``maxgram/types/message_stat.py``
- ``maxgram/types/linked_message.py``
- ``maxgram/types/recipient.py``
- ``maxgram/types/new_message_body.py``
- ``maxgram/types/new_message_link.py``
