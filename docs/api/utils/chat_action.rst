==================
ChatActionSender
==================

.. module:: maxgram.utils.chat_action

Утилита для отправки индикаторов действий.

.. code-block:: python

   class ChatActionSender:
       def __init__(
           self,
           *,
           action: str,
           chat_id: int,
           bot: Bot,
           interval: float = 5.0,
           initial_sleep: float = 0.0,
       ) -> None: ...

Фабричные методы
----------------

.. code-block:: python

   ChatActionSender.typing(chat_id=..., bot=...)
   ChatActionSender.sending_photo(chat_id=..., bot=...)
   ChatActionSender.sending_video(chat_id=..., bot=...)
   ChatActionSender.sending_file(chat_id=..., bot=...)

Использование
-------------

.. code-block:: python

   async with ChatActionSender.typing(chat_id=chat_id, bot=bot):
       # "Печатает..." отображается, пока идёт обработка
       await asyncio.sleep(3)
       await message.answer(text="Done!")

Действие отправляется периодически (каждые ``interval`` секунд) пока
контекстный менеджер активен.

Исходный файл
--------------

``maxgram/utils/chat_action.py``
