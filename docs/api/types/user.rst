==============
Пользователи
==============

User
----

.. module:: maxgram.types.user

Базовая модель пользователя MAX.

.. code-block:: python

   class User(MaxObject):
       user_id: int
       first_name: str
       last_name: str | None = None
       username: str | None = None
       is_bot: bool = False
       last_activity_time: int | None = None
       name: str | None = None  # deprecated

Поля
^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Поле
     - Тип
     - Описание
   * - ``user_id``
     - ``int``
     - Уникальный ID пользователя
   * - ``first_name``
     - ``str``
     - Имя
   * - ``last_name``
     - ``str | None``
     - Фамилия
   * - ``username``
     - ``str | None``
     - Имя пользователя (без ``@``)
   * - ``is_bot``
     - ``bool``
     - Является ли ботом
   * - ``last_activity_time``
     - ``int | None``
     - Время последней активности (Unix timestamp)
   * - ``name``
     - ``str | None``
     - Полное имя (deprecated)

Свойства
^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Свойство
     - Тип
     - Описание
   * - ``full_name``
     - ``str``
     - ``"First Last"`` или ``"First"`` если нет фамилии
   * - ``mention_html``
     - ``str``
     - ``<a href="max://user/123">First Last</a>``
   * - ``mention_md``
     - ``str``
     - ``[First Last](max://user/123)``

Методы
^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Метод
     - Описание
   * - ``await get_profile_photo(chat_id, full_size=True)``
     - Скачать аватарку. Возвращает ``bytes | None``
   * - ``await get_profile_photo_url(chat_id, full_size=True)``
     - Получить URL аватарки. Возвращает ``str | None``

.. code-block:: python

   user = message.sender
   chat_id = message.recipient.chat_id

   user.full_name       # "Michael Smith"
   user.mention_html    # '<a href="max://user/123">Michael Smith</a>'

   await message.answer(text=f"Hello, {user.mention_html}!")

   # Скачать аватарку (bytes)
   photo = await user.get_profile_photo(chat_id=chat_id)
   if photo:
       with open("avatar.jpg", "wb") as f:
           f.write(photo)

   # Только URL без скачивания
   url = await user.get_profile_photo_url(chat_id=chat_id)

   # Миниатюра
   thumb = await user.get_profile_photo(chat_id=chat_id, full_size=False)

UserWithPhoto
-------------

.. module:: maxgram.types.user_with_photo

Пользователь с информацией об аватаре.

.. code-block:: python

   class UserWithPhoto(User):
       avatar_url: str | None = None
       full_avatar_url: str | None = None
       description: str | None = None

Дополнительные поля
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Поле
     - Тип
     - Описание
   * - ``avatar_url``
     - ``str | None``
     - URL аватара (уменьшенный)
   * - ``full_avatar_url``
     - ``str | None``
     - URL аватара (полный размер)
   * - ``description``
     - ``str | None``
     - Описание/биография

BotInfo
-------

.. module:: maxgram.types.bot_info

Информация о боте (ответ ``GET /me``).

.. code-block:: python

   class BotInfo(UserWithPhoto):
       commands: list[BotCommand] | None = None

Наследует все поля ``UserWithPhoto`` + ``User``.

ChatMember
----------

.. module:: maxgram.types.chat_member

Участник чата с дополнительной информацией о членстве.

.. code-block:: python

   class ChatMember(UserWithPhoto):
       last_access_time: int | None = None
       is_owner: bool = False
       is_admin: bool = False
       join_time: int | None = None
       permissions: list[str] | None = None
       alias: str | None = None

Поля
^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Поле
     - Тип
     - Описание
   * - ``last_access_time``
     - ``int | None``
     - Последнее посещение
   * - ``is_owner``
     - ``bool``
     - Владелец чата
   * - ``is_admin``
     - ``bool``
     - Администратор
   * - ``join_time``
     - ``int | None``
     - Время вступления
   * - ``permissions``
     - ``list[str] | None``
     - Права администратора
   * - ``alias``
     - ``str | None``
     - Псевдоним в чате

ChatAdmin
---------

.. module:: maxgram.types.chat_admin

Запрос на назначение администратора.

.. code-block:: python

   class ChatAdmin(MaxObject):
       user_id: int
       permissions: list[str] | None = None
       alias: str | None = None

BotCommand
----------

.. module:: maxgram.types.bot_command

Описание команды бота.

.. code-block:: python

   class BotCommand(MaxObject):
       name: str
       description: str

Исходные файлы
--------------

- ``maxgram/types/user.py``
- ``maxgram/types/user_with_photo.py``
- ``maxgram/types/bot_info.py``
- ``maxgram/types/chat_member.py``
- ``maxgram/types/chat_admin.py``
- ``maxgram/types/bot_command.py``
