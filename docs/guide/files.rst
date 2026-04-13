==================
Работа с файлами
==================

pymaxgram поддерживает загрузку файлов из различных источников.

Типы InputFile
--------------

BufferedInputFile
^^^^^^^^^^^^^^^^^

Загрузка из байтов (данные в памяти):

.. code-block:: python

   from maxgram.types import BufferedInputFile

   # Из байтов
   file = BufferedInputFile(
       file=b"Hello, World!",
       filename="hello.txt",
   )

   # Из файла на диске (загружает в память)
   file = BufferedInputFile.from_file("path/to/file.txt")

FSInputFile
^^^^^^^^^^^

Асинхронная потоковая загрузка из файловой системы:

.. code-block:: python

   from maxgram.types import FSInputFile

   file = FSInputFile(
       path="path/to/large_file.mp4",
       filename="video.mp4",    # Опционально
       chunk_size=64 * 1024,    # Размер чанка (64KB по умолчанию)
   )

.. note::

   ``FSInputFile`` использует ``aiofiles`` для асинхронного чтения,
   что эффективнее для больших файлов.

URLInputFile
^^^^^^^^^^^^

Потоковая загрузка по URL:

.. code-block:: python

   from maxgram.types import URLInputFile

   file = URLInputFile(
       url="https://example.com/image.jpg",
       filename="image.jpg",      # Опционально
       headers={"Auth": "token"}, # Дополнительные заголовки
       timeout=30,                # Таймаут (секунды)
   )

Двухэтапная загрузка
---------------------

MAX API использует двухэтапную загрузку файлов:

1. Получить URL для загрузки
2. Загрузить файл и получить токен

.. code-block:: python

   # Упрощённый способ через Bot
   token = await bot.upload_file(
       file_type="image",     # "image", "video", "audio", "file"
       file_data=b"...",      # Байты файла
       filename="photo.jpg",
   )

   # Использование токена в вложении
   from maxgram.types import Attachment

   await message.answer(
       text="Вот ваше фото:",
       attachments=[
           Attachment(
               type="image",
               payload={"token": token},
           )
       ],
   )

Ручная двухэтапная загрузка
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Шаг 1: Получить URL
   upload_info = await bot.get_upload_url(type="image")
   print(upload_info.url)    # URL для загрузки
   print(upload_info.token)  # Токен (может быть None)

   # Шаг 2: Загрузить файл
   result = await bot.session.upload_file(
       bot=bot,
       upload_url=upload_info.url,
       file_data=file_bytes,
       filename="photo.jpg",
   )

Типы загрузки
-------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Тип
     - Описание
   * - ``image``
     - Изображения (JPEG, PNG и т.д.)
   * - ``video``
     - Видеофайлы
   * - ``audio``
     - Аудиофайлы
   * - ``file``
     - Любые файлы

Константы
---------

.. code-block:: python

   from maxgram.types.input_file import DEFAULT_CHUNK_SIZE

   DEFAULT_CHUNK_SIZE = 64 * 1024  # 65536 байт (64 КБ)
