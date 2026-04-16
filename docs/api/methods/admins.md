# Администраторы

## GetAdmins

`GET /chats/{chat_id}/members/admins` → `list[ChatMember]`

```python
class GetAdmins(MaxMethod[list[ChatMember]]):
    chat_id: int
    marker: int | None = None
```

## AssignAdmins

`POST /chats/{chat_id}/members/admins` → `bool`

```python
class AssignAdmins(MaxMethod[bool]):
    chat_id: int
    admins: list[dict[str, Any]]
```

Пример:

```python
await bot.assign_admins(
    chat_id=123,
    admins=[
        {"user_id": 456, "permissions": ["read_all_messages", "pin_message"]},
    ],
)
```

## RemoveAdmin

`DELETE /chats/{chat_id}/members/admins/{user_id}` → `bool`

```python
class RemoveAdmin(MaxMethod[bool]):
    chat_id: int
    user_id: int
```

## Исходные файлы

- `maxgram/methods/get_admins.py`
- `maxgram/methods/assign_admins.py`
- `maxgram/methods/remove_admin.py`
