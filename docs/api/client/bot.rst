=========
Bot
=========

.. module:: maxgram.client.bot

Класс ``Bot`` — главный клиент для взаимодействия с MAX Bot API.

Определение
-----------

.. code-block:: python

   class Bot:
       def __init__(
           self,
           token: str,
           session: Any | None = None,
           default: DefaultBotProperties | None = None,
           **kwargs: Any,
       ) -> None: ...

Параметры конструктора
^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Параметр
     - Тип
     - Описание
   * - ``token``
     - ``str``
     - Токен бота. Обязательный. Выбрасывает ``ValueError`` если пустой
   * - ``session``
     - ``Any | None``
     - HTTP-сессия. По умолчанию ``AiohttpSession()``
   * - ``default``
     - ``DefaultBotProperties | None``
     - Настройки по умолчанию для сообщений
   * - ``**kwargs``
     - ``Any``
     - Произвольные параметры, сохраняются как атрибуты экземпляра

Свойства
--------

.. list-table::
   :header-rows: 1
   :widths: 15 20 65

   * - Имя
     - Тип
     - Описание
   * - ``token``
     - ``str``
     - Токен бота (read-only, через ``__token`` private attr)
   * - ``id``
     - ``int | None``
     - ID бота из ``_me.user_id``. ``None`` до первого ``get_me()``
   * - ``username``
     - ``str | None``
     - Username бота из ``_me.username``. ``None`` до первого ``get_me()``
   * - ``session``
     - ``BaseSession``
     - HTTP-сессия
   * - ``default``
     - ``DefaultBotProperties``
     - Настройки по умолчанию
   * - ``_me``
     - ``BotInfo | None``
     - Кэш информации о боте

Специальные методы
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Метод
     - Описание
   * - ``__call__(method: MaxMethod[T]) -> T``
     - Выполняет API-метод через сессию
   * - ``__hash__() -> int``
     - Хэш на основе токена
   * - ``__eq__(other) -> bool``
     - Сравнение по токену
   * - ``__aenter__() -> Bot``
     - Вход в async context manager
   * - ``__aexit__()``
     - Закрывает сессию

API-методы
----------

Информация о боте
^^^^^^^^^^^^^^^^^^

- ``get_me() -> BotInfo``
- ``me() -> BotInfo`` — кэшированная версия

Чаты
^^^^

- ``get_chats(count?, marker?) -> list[Chat]``
- ``get_chat(chat_id) -> Chat``
- ``edit_chat(chat_id, title?, icon?, pin?, notify?) -> Chat``
- ``delete_chat(chat_id) -> bool``

Действия
^^^^^^^^

- ``send_action(chat_id, action) -> bool``

Закреплённые сообщения
^^^^^^^^^^^^^^^^^^^^^^

- ``get_pinned_message(chat_id) -> Message | None``
- ``pin_message(chat_id, message_id, notify?) -> bool``
- ``unpin_message(chat_id) -> bool``

Участники
^^^^^^^^^

- ``get_members(chat_id, user_ids?, marker?, count?) -> list[ChatMember]``
- ``add_members(chat_id, user_ids) -> bool``
- ``remove_member(chat_id, user_id, block?) -> bool``
- ``get_my_membership(chat_id) -> ChatMember``
- ``leave_chat(chat_id) -> bool``

Администраторы
^^^^^^^^^^^^^^

- ``get_admins(chat_id, marker?) -> list[ChatMember]``
- ``assign_admins(chat_id, admins) -> bool``
- ``remove_admin(chat_id, user_id) -> bool``

Подписки
^^^^^^^^

- ``get_subscriptions() -> list[Subscription]``
- ``create_subscription(url, update_types?, secret?) -> bool``
- ``delete_subscription(url) -> bool``

Обновления
^^^^^^^^^^

- ``get_updates(limit?, timeout?, marker?, types?) -> list[Update]``

Сообщения
^^^^^^^^^

- ``send_message(chat_id?, user_id?, text?, attachments?, link?, notify?, format?, disable_link_preview?, keyboard?) -> Message``
- ``edit_message(message_id, text?, attachments?, notify?, format?, keyboard?) -> bool``
- ``delete_message(message_id) -> bool``
- ``get_messages(chat_id?, message_ids?, count?) -> list[Message]``
- ``get_message_by_id(message_id) -> Message``

Загрузка файлов
^^^^^^^^^^^^^^^

- ``get_upload_url(type) -> UploadInfo``
- ``upload_file(file_type, file_data, filename?) -> str``

Видео
^^^^^

- ``get_video_info(video_token) -> VideoInfo``

Callback
^^^^^^^^

- ``answer_callback(callback_id, text?, attachments?, notification?, notify?, format?, keyboard?) -> bool``

Исходный файл
--------------

``maxgram/client/bot.py``
