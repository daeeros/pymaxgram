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

Информация о видео.

```python
class VideoUrls(MaxObject):
    urls: dict[str, str] | None = None

class VideoInfo(MaxObject):
    token: str
    urls: VideoUrls | None = None
    thumbnail: Any | None = None
    width: int = 0
    height: int = 0
    duration: int = 0
```

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
