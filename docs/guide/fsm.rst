=============================
Конечные автоматы (FSM)
=============================

FSM (Finite State Machine) позволяет создавать пошаговые сценарии взаимодействия
с пользователем.

Определение состояний
---------------------

.. code-block:: python

   from maxgram.fsm.state import State, StatesGroup

   class RegistrationStates(StatesGroup):
       waiting_name = State()
       waiting_age = State()
       waiting_confirm = State()

Группы состояний могут быть вложенными:

.. code-block:: python

   class MainStates(StatesGroup):
       idle = State()

       class Registration(StatesGroup):
           name = State()
           age = State()

FSMContext
---------

:class:`~maxgram.fsm.context.FSMContext` предоставляет интерфейс для управления
состоянием и данными пользователя.

Методы:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Метод
     - Описание
   * - ``await set_state(state)``
     - Установить текущее состояние
   * - ``await get_state()``
     - Получить текущее состояние (строка или ``None``)
   * - ``await set_data(data)``
     - Заменить все данные
   * - ``await get_data()``
     - Получить все данные (``dict``)
   * - ``await get_value(key, default)``
     - Получить значение по ключу
   * - ``await update_data(**kwargs)``
     - Обновить данные (merge)
   * - ``await clear()``
     - Сбросить состояние и данные

Пример: пошаговая регистрация
------------------------------

.. code-block:: python

   from maxgram import Router
   from maxgram.filters import Command, StateFilter
   from maxgram.fsm.state import State, StatesGroup
   from maxgram.fsm.context import FSMContext

   router = Router()

   class Reg(StatesGroup):
       waiting_name = State()
       waiting_age = State()

   @router.message(Command("register"))
   async def start_reg(message, state: FSMContext, bot):
       await state.set_state(Reg.waiting_name)
       await message.answer(text="Как вас зовут?")

   @router.message(StateFilter(Reg.waiting_name))
   async def get_name(message, state: FSMContext, bot):
       await state.update_data(name=message.body.text)
       await state.set_state(Reg.waiting_age)
       await message.answer(text="Сколько вам лет?")

   @router.message(StateFilter(Reg.waiting_age))
   async def get_age(message, state: FSMContext, bot):
       try:
           age = int(message.body.text)
       except ValueError:
           await message.answer(text="Введите число.")
           return

       await state.update_data(age=age)
       data = await state.get_data()
       await state.clear()
       await message.answer(
           text=f"Регистрация завершена!\nИмя: {data['name']}\nВозраст: {age}"
       )

Стратегии FSM
--------------

Стратегия определяет, как формируется ключ хранилища:

.. code-block:: python

   from maxgram import Dispatcher
   from maxgram.fsm.strategy import FSMStrategy

   dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Стратегия
     - Описание
   * - ``USER_IN_CHAT``
     - Состояние привязано к паре (пользователь, чат). **По умолчанию**
   * - ``CHAT``
     - Общее состояние для всего чата
   * - ``GLOBAL_USER``
     - Глобальное состояние пользователя (во всех чатах)
   * - ``USER_IN_TOPIC``
     - Состояние привязано к (пользователь, чат, топик)
   * - ``CHAT_TOPIC``
     - Состояние привязано к (чат, топик)

Хранилища (Storage)
--------------------

MemoryStorage
^^^^^^^^^^^^^

Хранит данные в оперативной памяти. Используется по умолчанию.

.. code-block:: python

   from maxgram.fsm.storage.memory import MemoryStorage

   dp = Dispatcher(storage=MemoryStorage())

.. warning::

   Данные ``MemoryStorage`` теряются при перезапуске бота. Для продакшена
   реализуйте свой ``BaseStorage`` (например, на основе Redis).

Пользовательское хранилище
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from maxgram.fsm.storage.base import BaseStorage, StorageKey

   class RedisStorage(BaseStorage):
       async def set_state(self, key: StorageKey, state: str | None = None) -> None:
           ...

       async def get_state(self, key: StorageKey) -> str | None:
           ...

       async def set_data(self, key: StorageKey, data: dict) -> None:
           ...

       async def get_data(self, key: StorageKey) -> dict:
           ...

       async def close(self) -> None:
           ...

StorageKey
^^^^^^^^^^

Ключ для идентификации данных в хранилище:

.. code-block:: python

   from maxgram.fsm.storage.base import StorageKey

   StorageKey(
       bot_id: int,     # ID бота
       chat_id: int,    # ID чата
       user_id: int,    # ID пользователя
       destiny: str = "default",  # Дополнительный идентификатор
   )

Изоляция событий
-----------------

Для предотвращения гонок при одновременных обновлениях:

.. code-block:: python

   from maxgram.fsm.storage.memory import SimpleEventIsolation

   dp = Dispatcher(
       events_isolation=SimpleEventIsolation(),
   )

- ``DisabledEventIsolation`` — без изоляции (по умолчанию)
- ``SimpleEventIsolation`` — asyncio.Lock на каждый StorageKey

Отключение FSM
--------------

.. code-block:: python

   dp = Dispatcher(disable_fsm=True)
