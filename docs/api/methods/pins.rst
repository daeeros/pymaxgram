========================
Закреплённые сообщения
========================

GetPinnedMessage
----------------

``GET /chats/{chat_id}/pin`` → ``Message | None``

.. code-block:: python

   class GetPinnedMessage(MaxMethod[Message | None]):
       chat_id: int

PinMessage
----------

``PUT /chats/{chat_id}/pin`` → ``bool``

.. code-block:: python

   class PinMessage(MaxMethod[bool]):
       chat_id: int
       message_id: str
       notify: bool | None = None

UnpinMessage
------------

``DELETE /chats/{chat_id}/pin`` → ``bool``

.. code-block:: python

   class UnpinMessage(MaxMethod[bool]):
       chat_id: int

Исходные файлы
--------------

- ``maxgram/methods/get_pinned_message.py``
- ``maxgram/methods/pin_message.py``
- ``maxgram/methods/unpin_message.py``
