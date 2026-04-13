==========
Command
==========

.. module:: maxgram.filters.command

Command
-------

Фильтр текстовых команд.

.. code-block:: python

   class Command(Filter):
       def __init__(
           self,
           *commands: str | re.Pattern,
           prefix: str = "/",
           ignore_case: bool = False,
           ignore_mention: bool = False,
           magic: MagicFilter | None = None,
       ) -> None: ...

Параметры
^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Параметр
     - Тип
     - Описание
   * - ``commands``
     - ``str | Pattern``
     - Имена команд (без префикса) или regex
   * - ``prefix``
     - ``str``
     - Префикс (``"/"``)
   * - ``ignore_case``
     - ``bool``
     - Без учёта регистра
   * - ``ignore_mention``
     - ``bool``
     - Игнорировать @mention
   * - ``magic``
     - ``MagicFilter | None``
     - Дополнительный фильтр на ``CommandObject``

При совпадении инъектирует ``command: CommandObject`` в обработчик.

CommandObject
-------------

.. code-block:: python

   @dataclass
   class CommandObject:
       prefix: str = "/"
       command: str = ""
       mention: str | None = None
       args: str | None = None
       regexp_match: re.Match | None = None
       magic_result: Any = None

Исходный файл
--------------

``maxgram/filters/command.py``
