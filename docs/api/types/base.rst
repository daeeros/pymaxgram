===============
Базовые типы
===============

.. module:: maxgram.types.base

MaxObject
---------

Базовый класс для всех типов данных MAX API.

.. code-block:: python

   class MaxObject(BotContextController, BaseModel):
       model_config = ConfigDict(
           frozen=True,
           extra="allow",
           validate_assignment=True,
           populate_by_name=True,
           arbitrary_types_allowed=True,
           defer_build=True,
       )

Особенности:

- **Frozen** (``frozen=True``) — объекты неизменяемы после создания
- **Extra allow** — принимает дополнительные поля из API
- **BotContextController** — предоставляет доступ к ``bot`` через контекст модели
- **UNSET-фильтрация** — model_validator (before) удаляет поля со значением ``UNSET``

MutableMaxObject
----------------

Изменяемая версия MaxObject:

.. code-block:: python

   class MutableMaxObject(MaxObject):
       model_config = ConfigDict(frozen=False)

Используется для типов, которые нужно модифицировать (например, ``ErrorEvent``).

UNSET
-----

Специальный sentinel-объект для различения ``None`` и "не передано":

.. code-block:: python

   from maxgram.types.base import UNSET, UNSET_TYPE

   UNSET = sentinel.UNSET        # Значение
   UNSET_TYPE = type(UNSET)      # Тип

Используется в ``MaxMethod`` и ``Dispatcher`` для определения,
был ли параметр передан явно.

Исходный файл
--------------

``maxgram/types/base.py``
