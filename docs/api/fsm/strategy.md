# FSMStrategy

Стратегия формирования ключа FSM.

```python
class FSMStrategy(str, Enum):
    USER_IN_CHAT = "user_in_chat"
    CHAT = "chat"
    GLOBAL_USER = "global_user"
    USER_IN_TOPIC = "user_in_topic"
    CHAT_TOPIC = "chat_topic"
```

## Описание стратегий

| Стратегия | Формирование ключа |
| --- | --- |
| `USER_IN_CHAT` | `(bot_id, chat_id, user_id)` — **по умолчанию**. Каждый пользователь имеет отдельное состояние в каждом чате |
| `CHAT` | `(bot_id, chat_id, chat_id)` — общее состояние для всего чата |
| `GLOBAL_USER` | `(bot_id, user_id, user_id)` — глобальное состояние пользователя |
| `USER_IN_TOPIC` | `(bot_id, chat_id:topic, user_id)` — привязано к топику |
| `CHAT_TOPIC` | `(bot_id, chat_id:topic, chat_id:topic)` — привязано к топику чата |

## apply_strategy

```python
def apply_strategy(
    strategy: FSMStrategy,
    event_context: EventContext,
    bot_id: int,
) -> StorageKey
```

Применяет стратегию к контексту события и возвращает `StorageKey`.

## Исходный файл

`maxgram/fsm/strategy.py`
