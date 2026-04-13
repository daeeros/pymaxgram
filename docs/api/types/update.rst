========
Update
========

.. module:: maxgram.types.update

Входящее обновление от MAX API.

.. code-block:: python

   class Update(MaxObject):
       update_type: str
       timestamp: int = 0
       message: Message | None = None
       callback: Callback | None = None
       user: User | None = None
       chat_id: int | None = None
       user_locale: str | None = None
       payload: str | None = None

Поля
----

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Поле
     - Тип
     - Описание
   * - ``update_type``
     - ``str``
     - Тип обновления (см. ниже)
   * - ``timestamp``
     - ``int``
     - Время обновления
   * - ``message``
     - ``Message | None``
     - Сообщение (для ``message_created``)
   * - ``callback``
     - ``Callback | None``
     - Callback (для ``message_callback``)
   * - ``user``
     - ``User | None``
     - Пользователь (для ``bot_started``)
   * - ``chat_id``
     - ``int | None``
     - ID чата (для ``bot_started``)
   * - ``user_locale``
     - ``str | None``
     - Локаль пользователя
   * - ``payload``
     - ``str | None``
     - Payload (для deep link)

Свойства
--------

event_type
^^^^^^^^^^

.. code-block:: python

   @property
   def event_type(self) -> str

Возвращает ``update_type``. Используется диспетчером для маршрутизации.

event
^^^^^

.. code-block:: python

   @property
   def event(self) -> Any

Возвращает объект события в зависимости от типа:

- ``message_created`` → ``self.message`` (``Message``)
- ``message_callback`` → ``self.callback`` (``Callback``)
- ``bot_started`` → ``self`` (``Update``)

Выбрасывает ``UpdateTypeLookupError`` при неизвестном типе.

Типы обновлений
---------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Тип
     - Описание
   * - ``message_created``
     - Новое сообщение в чате
   * - ``message_callback``
     - Нажатие inline-кнопки
   * - ``bot_started``
     - Пользователь запустил бота (нажал «Начать»)

UpdateTypeLookupError
---------------------

.. code-block:: python

   class UpdateTypeLookupError(Exception):
       pass

Выбрасывается при попытке получить ``event`` для неизвестного ``update_type``.

Исходный файл
--------------

``maxgram/types/update.py``
