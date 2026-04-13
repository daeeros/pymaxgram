=================
Действия в чате
=================

SendAction
----------

``POST /chats/{chat_id}/actions`` → ``bool``

Отправляет индикатор действия в чат.

.. code-block:: python

   class SendAction(MaxMethod[bool]):
       chat_id: int
       action: str

Доступные значения ``action`` (``ChatAction``):

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Значение
     - Описание
   * - ``typing_on``
     - Бот печатает
   * - ``sending_photo``
     - Бот отправляет фото
   * - ``sending_video``
     - Бот отправляет видео
   * - ``sending_audio``
     - Бот отправляет аудио
   * - ``sending_file``
     - Бот отправляет файл
   * - ``mark_seen``
     - Бот прочитал сообщения

Исходный файл
--------------

``maxgram/methods/send_action.py``
