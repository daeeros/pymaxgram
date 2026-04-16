# API Методы

Все 31 метод MAX Bot API, реализованные как классы `MaxMethod[T]`.

## Сводная таблица

| Класс | HTTP | API путь | Возврат | Раздел |
|-------|------|----------|---------|--------|
| `GetMe` | GET | `/me` | `BotInfo` | [bot_info](bot_info.md) |
| `SendMessage` | POST | `/messages` | `Message` | [messages](messages.md) |
| `EditMessage` | PUT | `/messages` | `bool` | [messages](messages.md) |
| `DeleteMessage` | DELETE | `/messages` | `bool` | [messages](messages.md) |
| `GetMessages` | GET | `/messages` | `list[Message]` | [messages](messages.md) |
| `GetMessageById` | GET | `/messages/{id}` | `Message` | [messages](messages.md) |
| `GetChat` | GET | `/chats/{id}` | `Chat` | [chats](chats.md) |
| `GetChats` | GET | `/chats` | `list[Chat]` | [chats](chats.md) |
| `EditChat` | PATCH | `/chats/{id}` | `Chat` | [chats](chats.md) |
| `DeleteChat` | DELETE | `/chats/{id}` | `bool` | [chats](chats.md) |
| `GetMembers` | GET | `/chats/{id}/members` | `list[ChatMember]` | [members](members.md) |
| `AddMembers` | POST | `/chats/{id}/members` | `bool` | [members](members.md) |
| `RemoveMember` | DELETE | `/chats/{id}/members` | `bool` | [members](members.md) |
| `GetMyMembership` | GET | `/chats/{id}/members/me` | `ChatMember` | [members](members.md) |
| `LeaveChat` | DELETE | `/chats/{id}/members/me` | `bool` | [members](members.md) |
| `GetAdmins` | GET | `/chats/{id}/members/admins` | `list[ChatMember]` | [admins](admins.md) |
| `AssignAdmins` | POST | `/chats/{id}/members/admins` | `bool` | [admins](admins.md) |
| `RemoveAdmin` | DELETE | `/chats/{id}/members/admins/{uid}` | `bool` | [admins](admins.md) |
| `AnswerCallback` | POST | `/answers` | `bool` | [callbacks](callbacks.md) |
| `GetSubscriptions` | GET | `/subscriptions` | `list[Subscription]` | [subscriptions](subscriptions.md) |
| `CreateSubscription` | POST | `/subscriptions` | `bool` | [subscriptions](subscriptions.md) |
| `DeleteSubscription` | DELETE | `/subscriptions` | `bool` | [subscriptions](subscriptions.md) |
| `GetUpdates` | GET | `/updates` | `list[Update]` | [updates](updates.md) |
| `GetUploadUrl` | POST | `/uploads` | `UploadInfo` | [uploads](uploads.md) |
| `GetVideoInfo` | GET | `/videos/{token}` | `VideoInfo` | [uploads](uploads.md) |
| `GetPinnedMessage` | GET | `/chats/{id}/pin` | `Message\|None` | [pins](pins.md) |
| `PinMessage` | PUT | `/chats/{id}/pin` | `bool` | [pins](pins.md) |
| `UnpinMessage` | DELETE | `/chats/{id}/pin` | `bool` | [pins](pins.md) |
| `SendAction` | POST | `/chats/{id}/actions` | `bool` | [actions](actions.md) |
