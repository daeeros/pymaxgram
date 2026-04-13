==========
Storage
==========

.. module:: maxgram.fsm.storage

StorageKey
----------

.. code-block:: python

   @dataclass(frozen=True)
   class StorageKey:
       bot_id: int
       chat_id: int
       user_id: int
       destiny: str = "default"

BaseStorage
-----------

Абстрактное хранилище FSM.

.. code-block:: python

   class BaseStorage(ABC):
       @abstractmethod
       async def set_state(self, key: StorageKey, state: str | None = None) -> None: ...

       @abstractmethod
       async def get_state(self, key: StorageKey) -> str | None: ...

       @abstractmethod
       async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None: ...

       @abstractmethod
       async def get_data(self, key: StorageKey) -> dict[str, Any]: ...

       @abstractmethod
       async def close(self) -> None: ...

       # Конкретные методы (вызывают абстрактные)
       async def get_value(self, key, field, default=None) -> Any: ...
       async def update_data(self, key, data=None, **kwargs) -> dict: ...

MemoryStorage
-------------

Хранилище в оперативной памяти.

.. code-block:: python

   class MemoryStorage(BaseStorage):
       ...

.. warning::

   Данные теряются при перезапуске. Не для продакшена.

Event Isolation
---------------

BaseEventIsolation
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class BaseEventIsolation(ABC):
       @abstractmethod
       async def lock(self, key: StorageKey) -> AsyncContextManager: ...

       @abstractmethod
       async def close(self) -> None: ...

DisabledEventIsolation
^^^^^^^^^^^^^^^^^^^^^^

No-op изоляция (по умолчанию).

SimpleEventIsolation
^^^^^^^^^^^^^^^^^^^^

``asyncio.Lock`` на каждый ``StorageKey``.

Исходные файлы
--------------

- ``maxgram/fsm/storage/base.py``
- ``maxgram/fsm/storage/memory.py``
