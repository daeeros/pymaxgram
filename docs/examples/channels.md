# Каналы

Бот может получать посты канала и отвечать на них.

## Требования

Бот должен быть **администратором канала**. Достаточно прав `read_all_messages`
и `write` — право `post_edit_delete_message` для ответов не требуется.

## Как приходит пост

Пост канала доставляется обычным событием `message_created`, отдельного типа
апдейта для каналов в MAX нет:

```json
{
  "update_type": "message_created",
  "message": {
    "recipient": {"chat_id": -73707052027205, "chat_type": "channel"},
    "body": {"mid": "mid.ffff...", "seq": 117133882195118147, "text": "Текст поста"}
  }
}
```

Особенности:

- `sender` отсутствует — пост публикуется от имени канала, а не пользователя;
- `stat` и `url` во входящем апдейте **не заполняются**, несмотря на описание в
  API-справочнике, поэтому определять канал нужно по `recipient.chat_type`;
- собственные сообщения бота обратно как `message_created` не приходят, так что
  обработчик не зациклится на своих же ответах.

## Обработчик

```python
import asyncio

from maxgram import Bot, Dispatcher
from maxgram.filters import ChannelPost
from maxgram.types import Message

bot = Bot("TOKEN")
dp = Dispatcher()


@dp.message(ChannelPost())
async def on_channel_post(message: Message):
    await message.reply(f"Новый пост: {message.body.text}")


asyncio.run(dp.start_polling(bot))
```

Без фильтра то же самое пишется через свойство:

```python
@dp.message()
async def on_message(message: Message):
    if not message.is_channel_post:
        return
    await message.reply("Комментарий от бота")
```

## Отправка в канал

Все три варианта работают:

```python
# Ответ на пост
await message.reply("комментарий")

# Отдельный пост от имени бота
await bot.send_message(chat_id=message.recipient.chat_id, text="новый пост")

# Пересылка поста
from maxgram.types import NewMessageLink

await bot.send_message(
    chat_id=message.recipient.chat_id,
    link=NewMessageLink(type="forward", mid=message.body.mid),
)
```

!!! warning "Пересылка не принимает текст"
    `POST /messages` с `link.type = "forward"` и непустым `text` возвращает
    `400 {"code": "proto.payload", "message": "errors.forward.text.not-empty"}`.
    Пересылку нужно отправлять без текста.

## Определение канала при добавлении бота

События `bot_added`, `bot_removed`, `user_added`, `user_removed` несут флаг
`is_channel`:

```python
@dp.bot_added()
async def on_bot_added(event):
    if event.is_channel:
        chat = await bot.get_chat(event.chat_id)
        print(chat.is_channel, chat.messages_count)
```
