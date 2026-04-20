# Типы данных

Все типы данных pymaxgram — это Pydantic v2 модели, наследующие от `MaxObject`.

## Иерархия наследования

```text
BaseModel + BotContextController
└── MaxObject (frozen)
    ├── MutableMaxObject (unfrozen)
    │   └── ErrorEvent
    ├── User
    │   └── UserWithPhoto
    │       ├── BotInfo
    │       └── ChatMember
    ├── Chat
    ├── Message
    ├── Callback
    ├── Update
    ├── MessageBody
    ├── MessageStat
    ├── LinkedMessage
    ├── Recipient
    ├── NewMessageBody
    ├── NewMessageLink
    ├── BotCommand
    ├── Image
    ├── Subscription
    ├── UploadInfo
    ├── VideoInfo, VideoUrls
    ├── ChatAdmin
    ├── Button
    ├── InlineKeyboard
    ├── Attachment
    │   ├── PhotoAttachment              (payload: PhotoAttachmentPayload)
    │   ├── VideoAttachment              (payload: VideoAttachmentPayload)
    │   ├── AudioAttachment              (payload: AudioAttachmentPayload)
    │   ├── FileAttachment               (payload: FileAttachmentPayload)
    │   ├── StickerAttachment            (payload: StickerAttachmentPayload)
    │   ├── ContactAttachment            (payload: ContactAttachmentPayload)
    │   ├── InlineKeyboardAttachment     (payload: ButtonsPayload)
    │   ├── LocationAttachment           (payload: LocationAttachmentPayload)
    │   └── ShareAttachment              (payload: ShareAttachmentPayload)
    ├── PhotoAttachmentPayload / VideoAttachmentPayload / ... / ButtonsPayload
    ├── AttachmentRequest
    │   ├── PhotoAttachmentRequest
    │   ├── VideoAttachmentRequest
    │   ├── AudioAttachmentRequest
    │   ├── FileAttachmentRequest
    │   └── InlineKeyboardAttachmentRequest
    └── InputFile (ABC, не Pydantic)
        ├── BufferedInputFile
        ├── FSInputFile
        └── URLInputFile
```
