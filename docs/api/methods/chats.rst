======
Чаты
======

GetChat
-------

``GET /chats/{chat_id}`` → ``Chat``

.. code-block:: python

   class GetChat(MaxMethod[Chat]):
       chat_id: int

GetChats
--------

``GET /chats`` → ``list[Chat]``

.. code-block:: python

   class GetChats(MaxMethod[list[Chat]]):
       count: int | None = None
       marker: int | None = None

EditChat
--------

``PATCH /chats/{chat_id}`` → ``Chat``

.. code-block:: python

   class EditChat(MaxMethod[Chat]):
       chat_id: int
       icon: dict[str, Any] | None = None
       title: str | None = None
       pin: str | None = None
       notify: bool | None = None

DeleteChat
----------

``DELETE /chats/{chat_id}`` → ``bool``

.. code-block:: python

   class DeleteChat(MaxMethod[bool]):
       chat_id: int

Исходные файлы
--------------

- ``maxgram/methods/get_chat.py``
- ``maxgram/methods/get_chats.py``
- ``maxgram/methods/edit_chat.py``
- ``maxgram/methods/delete_chat.py``
