# Вложения

Каждый тип вложения имеет свой типизированный `payload` и дополнительные поля.
Благодаря discriminated union pydantic сам парсит `{"type": "image", ...}` в
конкретный подкласс (`PhotoAttachment`, `VideoAttachment` и т.д.) при получении
сообщений.

## Типы вложений (Attachment)

### Attachment (базовый)

```python
class Attachment(MaxObject):
    type: str
    payload: Any | None = None
```

### Подтипы и их поля

| Класс | type | Поля сверх базовых |
| --- | --- | --- |
| `PhotoAttachment` | `"image"` | `payload: PhotoAttachmentPayload` |
| `VideoAttachment` | `"video"` | `payload: VideoAttachmentPayload`, `urls: VideoUrls`, `thumbnail: PhotoAttachmentPayload`, `width/height/duration: int` |
| `AudioAttachment` | `"audio"` | `payload: AudioAttachmentPayload`, `transcription: str` |
| `FileAttachment` | `"file"` | `payload: FileAttachmentPayload`, `filename: str`, `size: int` |
| `StickerAttachment` | `"sticker"` | `payload: StickerAttachmentPayload`, `width/height: int` |
| `ContactAttachment` | `"contact"` | `payload: ContactAttachmentPayload` |
| `InlineKeyboardAttachment` | `"inline_keyboard"` | `payload: ButtonsPayload` |
| `LocationAttachment` | `"location"` | `payload: LocationAttachmentPayload`, `latitude/longitude: float` |
| `ShareAttachment` | `"share"` | `payload: ShareAttachmentPayload`, `title/description/image_url: str` |

### Payload-классы

```python
class PhotoAttachmentPayload(MaxObject):
    photo_id: int | None = None
    token: str | None = None
    url: str | None = None


class VideoAttachmentPayload(MaxObject):
    token: str | None = None
    url: str | None = None


class AudioAttachmentPayload(MaxObject):
    token: str | None = None
    url: str | None = None


class FileAttachmentPayload(MaxObject):
    token: str | None = None
    url: str | None = None


class StickerAttachmentPayload(MaxObject):
    url: str | None = None
    code: str | None = None


class ContactAttachmentPayload(MaxObject):
    vcf_info: str | None = None
    max_info: User | None = None


class ShareAttachmentPayload(MaxObject):
    url: str | None = None
    token: str | None = None


class LocationAttachmentPayload(MaxObject):
    latitude: float | None = None
    longitude: float | None = None


class ButtonsPayload(MaxObject):
    buttons: list[list[ButtonUnion]] | None = None
```

`ButtonUnion` включает все 7 типов кнопок (`CallbackButton`, `LinkButton`,
`RequestContactButton`, `RequestGeoLocationButton`, `OpenAppButton`,
`MessageButton`, `ClipboardButton`) и тоже парсится через дискриминатор `type`.

### AttachmentUnion

```python
from typing import Annotated, Union
from pydantic import Field

AttachmentUnion = Annotated[
    Union[
        PhotoAttachment, VideoAttachment, AudioAttachment,
        FileAttachment, StickerAttachment, ContactAttachment,
        InlineKeyboardAttachment, LocationAttachment, ShareAttachment,
    ],
    Field(discriminator="type"),
]
```

`MessageBody.attachments` объявлен как `list[AttachmentUnion] | None`, поэтому
вложения приходят уже в виде правильного подкласса — без ручного разбора
`attachment.type`.

## Запросы вложений (AttachmentRequest)

Используются при отправке сообщений.

### AttachmentRequest (базовый)

```python
class AttachmentRequest(MaxObject):
    type: str
    payload: Any | None = None
```

### Подтипы

| Класс | type | Описание |
| --- | --- | --- |
| `PhotoAttachmentRequest` | `"image"` | Отправка изображения |
| `VideoAttachmentRequest` | `"video"` | Отправка видео |
| `AudioAttachmentRequest` | `"audio"` | Отправка аудио |
| `FileAttachmentRequest` | `"file"` | Отправка файла |
| `InlineKeyboardAttachmentRequest` | `"inline_keyboard"` | Отправка клавиатуры |

### InlineKeyboardAttachmentRequest

Дополнительный метод класса:

```python
@classmethod
def from_buttons(
    cls,
    buttons: list[list[Button]],
) -> InlineKeyboardAttachmentRequest
```

Создаёт вложение клавиатуры из двумерного списка кнопок.

## Примеры

### Приём входящих вложений

```python
from maxgram.types import (
    Message, PhotoAttachment, VideoAttachment, AudioAttachment,
)


@router.message()
async def handler(message: Message, bot):
    for a in message.body.attachments or []:
        if isinstance(a, PhotoAttachment):
            print(a.payload.url, a.payload.token)
        elif isinstance(a, VideoAttachment):
            print(a.width, a.height, a.duration, a.urls.mp4_720)
        elif isinstance(a, AudioAttachment):
            print(a.payload.token, a.transcription)
```

### Отправка вложений

```python
from maxgram.types import PhotoAttachmentRequest, InlineKeyboardAttachmentRequest
from maxgram.types import CallbackButton

# Изображение по токену
await message.answer(
    text="Photo:",
    attachments=[
        PhotoAttachmentRequest(payload={"token": "abc123"}),
    ],
)

# Inline-клавиатура
await message.answer(
    text="Choose:",
    attachments=[
        InlineKeyboardAttachmentRequest.from_buttons([
            [CallbackButton(text="Yes", payload="yes"),
             CallbackButton(text="No", payload="no")],
        ]),
    ],
)
```

## Исходные файлы

- `maxgram/types/attachment.py`
- `maxgram/types/attachment_request.py`
- `maxgram/types/button.py`
