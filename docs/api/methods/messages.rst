===========
Сообщения
===========

SendMessage
-----------

``POST /messages`` → ``Message``

.. code-block:: python

   class SendMessage(MaxMethod[Message]):
       chat_id: int | None = None
       user_id: int | None = None
       text: str | None = None
       attachments: list[Any] | None = None
       link: NewMessageLink | None = None
       notify: bool | None = None
       format: str | None = None
       disable_link_preview: bool | None = None

- ``chat_id`` / ``user_id`` передаются как query params
- ``text``, ``attachments``, ``link``, ``notify``, ``format`` — в теле запроса

EditMessage
-----------

``PUT /messages`` → ``bool``

.. code-block:: python

   class EditMessage(MaxMethod[bool]):
       message_id: str
       text: str | None = None
       attachments: list[Any] | None = None
       notify: bool | None = None
       format: str | None = None

- ``message_id`` передаётся как query param
- Остальное — в теле

DeleteMessage
-------------

``DELETE /messages`` → ``bool``

.. code-block:: python

   class DeleteMessage(MaxMethod[bool]):
       message_id: str

- ``message_id`` передаётся как query param

GetMessages
-----------

``GET /messages`` → ``list[Message]``

.. code-block:: python

   class GetMessages(MaxMethod[list[Message]]):
       chat_id: int | None = None
       message_ids: list[str] | None = None
       count: int | None = None

GetMessageById
--------------

``GET /messages/{message_id}`` → ``Message``

.. code-block:: python

   class GetMessageById(MaxMethod[Message]):
       message_id: str

Исходные файлы
--------------

- ``maxgram/methods/send_message.py``
- ``maxgram/methods/edit_message.py``
- ``maxgram/methods/delete_message.py``
- ``maxgram/methods/get_messages.py``
- ``maxgram/methods/get_message_by_id.py``
