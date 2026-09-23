# Информация о боте

## GetMe

`GET /me` → `BotInfo`

Получает информацию о текущем боте.

```python
class GetMe(MaxMethod[BotInfo]):
    pass  # Нет параметров
```

Возвращает `BotInfo` со всеми полями: `user_id`, `first_name`, `username`,
`avatar_url`, `commands` и т.д.

## Пример

```python
info = await bot.get_me()
print(f"Bot: {info.first_name} (@{info.username})")
print(f"ID: {info.user_id}")
if info.commands:
    for cmd in info.commands:
        print(f"  /{cmd.name} — {cmd.description}")
```

## EditBotCommands

`PATCH /me/commands` → `list[BotCommand]`

Устанавливает команды бота (до 32). Пустой список удаляет все команды.

```python
class EditBotCommands(MaxMethod[list[BotCommand]]):
    commands: list[BotCommand]
```

## Пример

```python
from maxgram.types import BotCommand

# Установить команды
await bot.set_commands([
    BotCommand(name="start", description="Запуск бота"),
    BotCommand(name="help", description="Справка"),
    BotCommand(name="settings", description="Настройки"),
])

# Удалить все команды
await bot.delete_commands()
```

## EditBotInfo

`PATCH /me` → `BotInfo`

!!! warning "Удалён в MAX API"
    MAX убрал `PATCH /me` — сервер отвечает `404 method.not.found`
    (`MaxNotFound`). Имя, описание и фото бота через Bot API больше не
    меняются. Для команд используйте `EditBotCommands` / `bot.set_commands()`.

```python
class EditBotInfo(MaxMethod[BotInfo]):
    name: str | None = None
    description: str | None = None
    commands: list[BotCommand] | None = None
    photo: dict[str, Any] | None = None
```

## Исходные файлы

- `maxgram/methods/get_me.py`
- `maxgram/methods/edit_bot_commands.py`
- `maxgram/methods/edit_bot_info.py`
