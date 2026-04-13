====================
DefaultBotProperties
====================

.. module:: maxgram.client.default

Настройки по умолчанию для отправки сообщений.

Определение
-----------

.. code-block:: python

   @dataclass
   class DefaultBotProperties:
       parse_mode: str | None = None
       disable_link_preview: bool | None = None
       notify: bool | None = None

Поля
----

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Поле
     - Тип
     - Описание
   * - ``parse_mode``
     - ``str | None``
     - Режим разметки: ``"html"`` или ``"markdown"`` (``ParseMode.HTML``, ``ParseMode.MARKDOWN``)
   * - ``disable_link_preview``
     - ``bool | None``
     - Отключить превью ссылок в сообщениях
   * - ``notify``
     - ``bool | None``
     - Отправлять уведомления получателям

Использование
-------------

.. code-block:: python

   from maxgram import Bot
   from maxgram.client.default import DefaultBotProperties
   from maxgram.enums import ParseMode

   bot = Bot(
       token="TOKEN",
       default=DefaultBotProperties(
           parse_mode=ParseMode.HTML,
           disable_link_preview=True,
           notify=False,
       ),
   )

   # Defaults автоматически применяются ко ВСЕМ методам отправки:
   # bot.send_message(), bot.edit_message(), bot.answer_callback(),
   # message.answer(), message.reply(), message.edit_text(), callback.answer()

   # HTML-разметка подставляется автоматически:
   await bot.send_message(chat_id=123, text="<b>Bold</b>")

   # Можно переопределить для конкретного вызова:
   await bot.send_message(chat_id=123, text="**Bold**", format=ParseMode.MARKDOWN)

BotContextController
--------------------

.. module:: maxgram.client.context_controller

Миксин для инъекции экземпляра Bot в Pydantic-модели.

.. code-block:: python

   class BotContextController:
       """
       Предоставляет доступ к Bot через Pydantic model context.
       Используется как базовый класс для MaxObject и MaxMethod.
       """

       def as_(self, bot: Bot) -> Self:
           """Привязывает объект к конкретному боту."""
           ...

       @property
       def bot(self) -> Bot:
           """Возвращает привязанный экземпляр Bot."""
           ...

Это позволяет типам данных (Message, Callback) вызывать методы API:

.. code-block:: python

   # Message.answer() использует self.bot для отправки
   await message.answer(text="Hello")
   # Эквивалентно:
   await bot.send_message(chat_id=message.recipient.chat_id, text="Hello")

Исходные файлы
--------------

- ``maxgram/client/default.py``
- ``maxgram/client/context_controller.py``
