==========
InputFile
==========

.. module:: maxgram.types.input_file

Типы файлов для загрузки.

InputFile (базовый)
-------------------

.. code-block:: python

   class InputFile(ABC):
       def __init__(
           self,
           filename: str | None = None,
           chunk_size: int = DEFAULT_CHUNK_SIZE,  # 64 * 1024
       ) -> None: ...

       @abstractmethod
       async def read(self, bot: Bot) -> AsyncGenerator[bytes, None]: ...

BufferedInputFile
-----------------

Загрузка из байтов в памяти.

.. code-block:: python

   class BufferedInputFile(InputFile):
       def __init__(
           self,
           file: bytes,
           filename: str,
           chunk_size: int = DEFAULT_CHUNK_SIZE,
       ) -> None: ...

       @classmethod
       def from_file(
           cls,
           path: str | Path,
           filename: str | None = None,
           chunk_size: int = DEFAULT_CHUNK_SIZE,
       ) -> BufferedInputFile: ...

Атрибут ``data: bytes`` — содержимое файла.

FSInputFile
-----------

Асинхронная потоковая загрузка из файловой системы.

.. code-block:: python

   class FSInputFile(InputFile):
       def __init__(
           self,
           path: str | Path,
           filename: str | None = None,
           chunk_size: int = DEFAULT_CHUNK_SIZE,
       ) -> None: ...

Атрибут ``path: str | Path`` — путь к файлу. Читает файл через ``aiofiles``.

URLInputFile
------------

Потоковая загрузка из URL.

.. code-block:: python

   class URLInputFile(InputFile):
       def __init__(
           self,
           url: str,
           headers: dict[str, Any] | None = None,
           filename: str | None = None,
           chunk_size: int = DEFAULT_CHUNK_SIZE,
           timeout: int = 30,
           bot: Bot | None = None,
       ) -> None: ...

Атрибуты:

- ``url: str`` — URL для загрузки
- ``headers: dict`` — HTTP-заголовки
- ``timeout: int`` — таймаут в секундах

Константы
---------

.. code-block:: python

   DEFAULT_CHUNK_SIZE = 64 * 1024  # 65536 байт (64 КБ)

Исходный файл
--------------

``maxgram/types/input_file.py``
