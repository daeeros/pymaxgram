============
API Методы
============

.. module:: maxgram.methods

Все 31 метод MAX Bot API, реализованные как классы ``MaxMethod[T]``.

Сводная таблица
---------------

.. list-table::
   :header-rows: 1
   :widths: 25 8 30 17 20

   * - Класс
     - HTTP
     - API путь
     - Возврат
     - Раздел
   * - ``GetMe``
     - GET
     - ``/me``
     - ``BotInfo``
     - :doc:`bot_info`
   * - ``SendMessage``
     - POST
     - ``/messages``
     - ``Message``
     - :doc:`messages`
   * - ``EditMessage``
     - PUT
     - ``/messages``
     - ``bool``
     - :doc:`messages`
   * - ``DeleteMessage``
     - DELETE
     - ``/messages``
     - ``bool``
     - :doc:`messages`
   * - ``GetMessages``
     - GET
     - ``/messages``
     - ``list[Message]``
     - :doc:`messages`
   * - ``GetMessageById``
     - GET
     - ``/messages/{id}``
     - ``Message``
     - :doc:`messages`
   * - ``GetChat``
     - GET
     - ``/chats/{id}``
     - ``Chat``
     - :doc:`chats`
   * - ``GetChats``
     - GET
     - ``/chats``
     - ``list[Chat]``
     - :doc:`chats`
   * - ``EditChat``
     - PATCH
     - ``/chats/{id}``
     - ``Chat``
     - :doc:`chats`
   * - ``DeleteChat``
     - DELETE
     - ``/chats/{id}``
     - ``bool``
     - :doc:`chats`
   * - ``GetMembers``
     - GET
     - ``/chats/{id}/members``
     - ``list[ChatMember]``
     - :doc:`members`
   * - ``AddMembers``
     - POST
     - ``/chats/{id}/members``
     - ``bool``
     - :doc:`members`
   * - ``RemoveMember``
     - DELETE
     - ``/chats/{id}/members``
     - ``bool``
     - :doc:`members`
   * - ``GetMyMembership``
     - GET
     - ``/chats/{id}/members/me``
     - ``ChatMember``
     - :doc:`members`
   * - ``LeaveChat``
     - DELETE
     - ``/chats/{id}/members/me``
     - ``bool``
     - :doc:`members`
   * - ``GetAdmins``
     - GET
     - ``/chats/{id}/members/admins``
     - ``list[ChatMember]``
     - :doc:`admins`
   * - ``AssignAdmins``
     - POST
     - ``/chats/{id}/members/admins``
     - ``bool``
     - :doc:`admins`
   * - ``RemoveAdmin``
     - DELETE
     - ``/chats/{id}/members/admins/{uid}``
     - ``bool``
     - :doc:`admins`
   * - ``AnswerCallback``
     - POST
     - ``/answers``
     - ``bool``
     - :doc:`callbacks`
   * - ``GetSubscriptions``
     - GET
     - ``/subscriptions``
     - ``list[Subscription]``
     - :doc:`subscriptions`
   * - ``CreateSubscription``
     - POST
     - ``/subscriptions``
     - ``bool``
     - :doc:`subscriptions`
   * - ``DeleteSubscription``
     - DELETE
     - ``/subscriptions``
     - ``bool``
     - :doc:`subscriptions`
   * - ``GetUpdates``
     - GET
     - ``/updates``
     - ``list[Update]``
     - :doc:`updates`
   * - ``GetUploadUrl``
     - POST
     - ``/uploads``
     - ``UploadInfo``
     - :doc:`uploads`
   * - ``GetVideoInfo``
     - GET
     - ``/videos/{token}``
     - ``VideoInfo``
     - :doc:`uploads`
   * - ``GetPinnedMessage``
     - GET
     - ``/chats/{id}/pin``
     - ``Message|None``
     - :doc:`pins`
   * - ``PinMessage``
     - PUT
     - ``/chats/{id}/pin``
     - ``bool``
     - :doc:`pins`
   * - ``UnpinMessage``
     - DELETE
     - ``/chats/{id}/pin``
     - ``bool``
     - :doc:`pins`
   * - ``SendAction``
     - POST
     - ``/chats/{id}/actions``
     - ``bool``
     - :doc:`actions`

.. toctree::
   :maxdepth: 1

   base
   messages
   chats
   members
   admins
   callbacks
   subscriptions
   updates
   uploads
   pins
   actions
   bot_info
