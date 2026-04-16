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

## EditBotInfo

`PATCH /me` → `BotInfo`

Изменяет информацию о боте.

```python
class EditBotInfo(MaxMethod[BotInfo]):
    name: str | None = None
    description: str | None = None
    commands: list[BotCommand] | None = None
    photo: dict[str, Any] | None = None
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

# Изменить описание
await bot.edit_info(description="Мой бот для MAX")

# Удалить все команды
await bot.delete_commands()
```

## Исходные файлы

- `maxgram/methods/get_me.py`
- `maxgram/methods/edit_bot_info.py`
