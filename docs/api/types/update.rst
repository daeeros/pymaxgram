========
Update
========

.. module:: maxgram.types.update

Входящее обновление от MAX API. Поля зависят от ``update_type``.

.. code-block:: python

   class Update(MaxObject):
       # Общие
       update_type: str
       timestamp: int = 0
       # Сообщения
       message: Message | None = None
       callback: Callback | None = None
       user_locale: str | None = None
       # Чат/бот/пользователь
       chat_id: int | None = None
       user: User | None = None
       payload: str | None = None
       title: str | None = None
       is_channel: bool | None = None
       inviter_id: int | None = None
       admin_id: int | None = None
       message_id: str | None = None
       user_id: int | None = None
       muted_until: int | None = None

Типы обновлений и их поля
--------------------------

**Сообщения:**

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - ``update_type``
     - Поля
     - Event
   * - ``message_created``
     - ``message``, ``user_locale?``
     - ``Message``
   * - ``message_callback``
     - ``callback``, ``message``, ``user_locale?``
     - ``Callback``
   * - ``message_edited``
     - ``message``
     - ``Message``
   * - ``message_removed``
     - ``message_id``, ``chat_id``, ``user_id``
     - ``Update``

**Бот:**

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - ``update_type``
     - Поля
     - Event
   * - ``bot_started``
     - ``chat_id``, ``user``, ``payload?``, ``user_locale?``
     - ``Update``
   * - ``bot_stopped``
     - ``chat_id``, ``user``, ``user_locale``
     - ``Update``
   * - ``bot_added``
     - ``chat_id``, ``user``, ``is_channel``
     - ``Update``
   * - ``bot_removed``
     - ``chat_id``, ``user``, ``is_channel``
     - ``Update``

**Пользователи и чат:**

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - ``update_type``
     - Поля
     - Event
   * - ``user_added``
     - ``chat_id``, ``user``, ``inviter_id?``, ``is_channel``
     - ``Update``
   * - ``user_removed``
     - ``chat_id``, ``user``, ``admin_id?``, ``is_channel``
     - ``Update``
   * - ``chat_title_changed``
     - ``chat_id``, ``user``, ``title``
     - ``Update``

**Диалоги:**

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - ``update_type``
     - Поля
     - Event
   * - ``dialog_muted``
     - ``chat_id``, ``user``, ``muted_until``, ``user_locale``
     - ``Update``
   * - ``dialog_unmuted``
     - ``chat_id``, ``user``, ``user_locale``
     - ``Update``
   * - ``dialog_cleared``
     - ``chat_id``, ``user``, ``user_locale``
     - ``Update``
   * - ``dialog_removed``
     - ``chat_id``, ``user``, ``user_locale``
     - ``Update``

Свойства
--------

event_type
^^^^^^^^^^

Возвращает ``update_type``. Используется диспетчером для маршрутизации.

event
^^^^^

Возвращает объект события:

- ``message_created`` → ``Message``
- ``message_callback`` → ``Callback`` (с заполненным ``callback.message``)
- ``message_edited`` → ``Message``
- Все остальные → ``Update`` (сам объект с полями ``chat_id``, ``user`` и т.д.)

Примеры
-------

.. code-block:: python

   @router.bot_started()
   async def on_start(event, bot):
       # event — это Update
       print(f"User {event.user.first_name} started bot")
       print(f"Chat: {event.chat_id}")
       if event.payload:
           print(f"Deep link: {event.payload}")

   @router.user_added()
   async def on_user_added(event, bot):
       print(f"{event.user.first_name} added to chat {event.chat_id}")
       if event.inviter_id:
           print(f"Invited by user {event.inviter_id}")

   @router.message_removed()
   async def on_removed(event, bot):
       print(f"Message {event.message_id} removed from chat {event.chat_id}")

UpdateTypeLookupError
---------------------

Выбрасывается при попытке получить ``event`` для неизвестного ``update_type``.

Исходный файл
--------------

``maxgram/types/update.py``
