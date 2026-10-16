# Комментарии

Комментарии к постам в каналах. `message_id` во всех методах — `mid` поста.
Бот должен быть администратором канала: чтение — с правом `read_all_messages`,
отправка — `read_all_messages` + `write`, удаление — `read_all_messages` + `delete`.
Вложения в комментариях не поддерживаются.

## GetComments

`GET /messages/{message_id}/comments` → `list[CommentMessage]`

```python
class GetComments(MaxMethod[list[CommentMessage]]):
    message_id: str
    comment_ids: list[str] | None = None  # если указан, пагинация игнорируется
    before: int | None = None             # Unix ms
    after: int | None = None              # Unix ms
    count: int | None = None              # 1–100, по умолчанию 50
```

Новые комментарии идут первыми.

## GetComment

`GET /messages/{message_id}/comments/{comment_id}` → `CommentMessage`

```python
class GetComment(MaxMethod[CommentMessage]):
    message_id: str
    comment_id: str
```

## SendComment

`POST /messages/{message_id}/comments` → `CommentMessage`

```python
class SendComment(MaxMethod[CommentMessage]):
    message_id: str
    text: str | None = None              # до 4000 символов
    link: NewMessageLink | None = None   # только reply, пересылка недоступна
    format: str | None = None            # "html" / "markdown"
    disable_link_preview: bool | None = None
```

- `disable_link_preview` — query param, остальное — тело запроса
- В комментариях не работают упоминания пользователей и гиперссылки
- В настройках канала должны быть включены комментарии

## EditComment

`PUT /messages/{message_id}/comments` → `bool`

```python
class EditComment(MaxMethod[bool]):
    message_id: str
    comment_id: str                      # query param
    text: str | None = None
    link: NewMessageLink | None = None
    format: str | None = None
```

- Редактировать можно только в течение 26 часов (иначе 422 `comments.timeout_exceeded`)
- Без права `edit` бот редактирует только свои комментарии

## DeleteComment

`DELETE /messages/{message_id}/comments` → `bool`

```python
class DeleteComment(MaxMethod[bool]):
    message_id: str
    comment_id: str                      # query param
```

## Методы Bot

```python
await bot.get_comments(post_mid, count=20)
await bot.get_comment(post_mid, comment_mid)
comment = await bot.send_comment(post_mid, "Спасибо!")
await bot.edit_comment(post_mid, comment.body.mid, text="Спасибо!!")
await bot.delete_comment(post_mid, comment.body.mid)
```

`send_comment` / `edit_comment` подставляют `DefaultBotProperties.parse_mode`,
`send_comment` — ещё и `disable_link_preview`.

## События

```python
@router.comment()                 # comment_created -> Message
async def on_comment(message: Message): ...

@router.comment_edited()          # comment_edited -> Message
async def on_comment_edited(message: Message): ...

@router.comment_removed()         # comment_removed -> CommentRemoved
async def on_comment_removed(event: CommentRemoved):
    event.post_id, event.message_id, event.user_id
```

## Исходные файлы

- `maxgram/methods/get_comments.py`
- `maxgram/methods/get_comment.py`
- `maxgram/methods/send_comment.py`
- `maxgram/methods/edit_comment.py`
- `maxgram/methods/delete_comment.py`
- `maxgram/types/comment_message.py`
