=================
Прочие типы
=================

Subscription
------------

.. module:: maxgram.types.subscription

Подписка на webhook.

.. code-block:: python

   class Subscription(MaxObject):
       url: str
       time: int = 0
       update_types: list[str] | None = None
       version: str | None = None

UploadInfo
----------

.. module:: maxgram.types.upload_info

Информация для загрузки файла.

.. code-block:: python

   class UploadInfo(MaxObject):
       url: str                    # URL для загрузки
       token: str | None = None    # Токен файла

VideoInfo
---------

.. module:: maxgram.types.video_info

Информация о видео.

.. code-block:: python

   class VideoUrls(MaxObject):
       urls: dict[str, str] | None = None

   class VideoInfo(MaxObject):
       token: str
       urls: VideoUrls | None = None
       thumbnail: Any | None = None
       width: int = 0
       height: int = 0
       duration: int = 0

ErrorEvent
----------

.. module:: maxgram.types.error_event

Обёртка для ошибки обработки.

.. code-block:: python

   class ErrorEvent(MutableMaxObject):
       update: Update
       exception: Exception

Используется ``ErrorsMiddleware`` для передачи ошибок в обработчики ``router.error``.

Исходные файлы
--------------

- ``maxgram/types/subscription.py``
- ``maxgram/types/upload_info.py``
- ``maxgram/types/video_info.py``
- ``maxgram/types/error_event.py``
