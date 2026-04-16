# Участники

## GetMembers

`GET /chats/{chat_id}/members` → `list[ChatMember]`

```python
class GetMembers(MaxMethod[list[ChatMember]]):
    chat_id: int
    user_ids: list[int] | None = None
    marker: int | None = None
    count: int | None = None
```

## AddMembers

`POST /chats/{chat_id}/members` → `bool`

```python
class AddMembers(MaxMethod[bool]):
    chat_id: int
    user_ids: list[int]
```

## RemoveMember

`DELETE /chats/{chat_id}/members` → `bool`

```python
class RemoveMember(MaxMethod[bool]):
    chat_id: int
    user_id: int
    block: bool | None = None
```

## GetMyMembership

`GET /chats/{chat_id}/members/me` → `ChatMember`

```python
class GetMyMembership(MaxMethod[ChatMember]):
    chat_id: int
```

## LeaveChat

`DELETE /chats/{chat_id}/members/me` → `bool`

```python
class LeaveChat(MaxMethod[bool]):
    chat_id: int
```

## Исходные файлы

- `maxgram/methods/get_members.py`
- `maxgram/methods/add_members.py`
- `maxgram/methods/remove_member.py`
- `maxgram/methods/get_my_membership.py`
- `maxgram/methods/leave_chat.py`
