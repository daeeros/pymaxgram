=============
Filter (ABC)
=============

.. module:: maxgram.filters.base

Абстрактный базовый класс для всех фильтров.

.. code-block:: python

   class Filter(ABC):
       async def __call__(self, *args: Any, **kwargs: Any) -> bool | dict[str, Any]:
           """
           Возвращает:
           - True — фильтр пройден
           - False — фильтр не пройден
           - dict — фильтр пройден + данные для инъекции в обработчик
           """
           ...

       def __invert__(self) -> Filter:
           """Инверсия: ~filter"""
           return _InvertFilter(self)

Создание пользовательского фильтра
------------------------------------

.. code-block:: python

   from maxgram.filters import Filter

   class IsAdmin(Filter):
       def __init__(self, admin_ids: set[int]):
           self.admin_ids = admin_ids

       async def __call__(self, message, **kwargs) -> bool:
           return message.sender and message.sender.user_id in self.admin_ids

   # С инъекцией данных
   class ExtractUserName(Filter):
       async def __call__(self, message, **kwargs) -> dict | bool:
           if message.sender:
               return {"user_name": message.sender.first_name}
           return False

Исходный файл
--------------

``maxgram/filters/base.py``
