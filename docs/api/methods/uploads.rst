=====================
Загрузка и видео
=====================

GetUploadUrl
------------

``POST /uploads`` → ``UploadInfo``

Получает URL для загрузки файла.

.. code-block:: python

   class GetUploadUrl(MaxMethod[UploadInfo]):
       type: str  # "image", "video", "audio", "file"

GetVideoInfo
------------

``GET /videos/{video_token}`` → ``VideoInfo``

Получает информацию о видео.

.. code-block:: python

   class GetVideoInfo(MaxMethod[VideoInfo]):
       video_token: str

Исходные файлы
--------------

- ``maxgram/methods/get_upload_url.py``
- ``maxgram/methods/get_video_info.py``
