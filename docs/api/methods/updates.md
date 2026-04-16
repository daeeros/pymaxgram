# Updates

## GetUpdates

`GET /updates` → `list[Update]`

Long polling для получения обновлений.

```python
class GetUpdates(MaxMethod[list[Update]]):
    limit: int | None = None
    timeout: int | None = None
    marker: int | None = None
    types: list[str] | None = None
```

### Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `limit` | `int \| None` | Максимальное количество обновлений |
| `timeout` | `int \| None` | Таймаут long polling (секунды) |
| `marker` | `int \| None` | Маркер для пагинации (курсор) |
| `types` | `list[str] \| None` | Фильтр типов обновлений |

!!! note
    Обычно `GetUpdates` вызывается автоматически диспетчером через `start_polling()`.

## Исходный файл

`maxgram/methods/get_updates.py`
