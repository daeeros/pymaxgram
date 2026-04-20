# Прочие типы

## Subscription

Подписка на webhook.

```python
class Subscription(MaxObject):
    url: str
    time: int = 0
    update_types: list[str] | None = None
    version: str | None = None
```

## UploadInfo

Информация для загрузки файла.

```python
class UploadInfo(MaxObject):
    url: str                    # URL для загрузки
    token: str | None = None    # Токен файла
```

## VideoInfo

Информация о видео, возвращаемая `GET /videos/{token}`.

```python
class VideoUrls(MaxObject):
    mp4_1080: str | None = None
    mp4_720: str | None = None
    mp4_480: str | None = None
    mp4_360: str | None = None
    mp4_240: str | None = None
    mp4_144: str | None = None
    hls: str | None = None


class VideoInfo(MaxObject):
    token: str
    urls: VideoUrls | None = None
    thumbnail: PhotoAttachmentPayload | None = None
    width: int = 0
    height: int = 0
    duration: int = 0
```

`VideoUrls` содержит плоские поля по разрешениям, `thumbnail` типизирован как
`PhotoAttachmentPayload` (см. [Вложения](./attachments.md)).

## ErrorEvent

Обёртка для ошибки обработки.

```python
class ErrorEvent(MutableMaxObject):
    update: Update
    exception: Exception
```

Используется `ErrorsMiddleware` для передачи ошибок в обработчики `router.error`.

## Исходные файлы

- `maxgram/types/subscription.py`
- `maxgram/types/upload_info.py`
- `maxgram/types/video_info.py`
- `maxgram/types/error_event.py`
