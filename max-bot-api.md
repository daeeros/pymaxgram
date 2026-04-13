# MAX Bot API — Полная документация

> Исчерпывающее руководство по использованию HTTP API мессенджера MAX для разработки чат-ботов.
> Источник: https://dev.max.ru/docs-api

---

## Оглавление

1. [Обзор](#обзор)
2. [Базовые принципы](#базовые-принципы)
3. [Авторизация](#авторизация)
4. [HTTP-коды ответов](#http-коды-ответов)
5. [Получение обновлений: Webhook vs Long Polling](#получение-обновлений-webhook-vs-long-polling)
6. [Клавиатура (inline-keyboard)](#клавиатура-inline-keyboard)
7. [Форматирование текста](#форматирование-текста)
8. [Методы API](#методы-api)
   - [bots](#bots)
   - [chats](#chats)
   - [subscriptions](#subscriptions)
   - [upload](#upload)
   - [messages](#messages)
   - [answers](#answers)
9. [Объекты](#объекты)

---

## Обзор

**MAX Bot API** — это HTTPS-интерфейс, через который боты взаимодействуют с платформой MAX. Обмен данными происходит в формате JSON.

**Базовый URL всех запросов:**
```
https://platform-api.max.ru
```

Каждый запрос — это вызов конкретного метода, соответствующего одному HTTP-глаголу:

| Метод  | Назначение                            |
| ------ | ------------------------------------- |
| GET    | Получить ресурс                       |
| POST   | Создать ресурс (например, сообщение)  |
| PUT    | Отредактировать ресурс                |
| PATCH  | Частично исправить ресурс             |
| DELETE | Удалить ресурс                        |

Параметры запроса передаются:
- в **пути** (`/chats/{chatId}`),
- в **query-параметрах** (`?chat_id=...&count=10`),
- в **теле** запроса (JSON, при `POST`, `PUT`, `PATCH`).

Сервер всегда возвращает JSON с запрошенными данными либо объект ошибки.

**Пример ответа для `GET /me`:**
```json
{
  "user_id": 1,
  "name": "My Bot",
  "username": "my_bot",
  "is_bot": true,
  "last_activity_time": 1737500130100
}
```

---

## Базовые принципы

- **Максимальная частота запросов**: 30 rps на `platform-api.max.ru`. Превышение даёт `429`.
- **Протокол**: только HTTPS. HTTP не поддерживается (в том числе для Webhook).
- Для **разработки и тестирования** используйте Long Polling.
- Для **production** — только Webhook.

---

## Авторизация

Токен бота создаётся на платформе [business.max.ru](https://business.max.ru/self) в разделе **Чат-боты → Интеграция → Получить токен**.

**Токен передаётся только через заголовок:**
```
Authorization: <access_token>
```

> ⚠️ Передача токена через query-параметры **больше не поддерживается**.

Токен следует хранить в секрете. Платформа может отозвать токен за нарушение правил.

---

## HTTP-коды ответов

| Код | Значение                          |
| --- | --------------------------------- |
| 200 | Успешная операция                 |
| 400 | Недействительный запрос           |
| 401 | Ошибка аутентификации             |
| 404 | Ресурс не найден                  |
| 405 | Метод не допускается              |
| 429 | Превышено количество запросов     |
| 503 | Сервис недоступен                 |

Многие методы, не возвращающие прикладной объект, отдают одну и ту же структуру:
```json
{
  "success": true,
  "message": "поясняющий текст, если success == false"
}
```

---

## Получение обновлений: Webhook vs Long Polling

Бот может получать входящие события (новые сообщения, нажатия кнопок и т. п.) одним из двух способов. Активны могут быть **только один из них одновременно**.

### Webhook (production)

- HTTPS POST-запрос на ваш endpoint с JSON-объектом [`Update`](#update).
- Endpoint должен быть доступен на **порту 443** (порт в URL не указывается).
- Сертификат **должен быть выдан доверенным CA** (самоподписанные для production-вебхуков не подходят — хотя в разделе "Подключение приложения" упоминается поддержка самоподписанных; при настройке проверяйте актуальную документацию).
- Доменное имя URL должно совпадать с CN/SAN сертификата.
- Endpoint должен отвечать **HTTP 200** в течение **30 секунд**.
- При указании `secret` в подписке сервер передаёт его в заголовке `X-Max-Bot-Api-Secret` — вы должны его проверять.

**Политика повторных попыток при неудаче доставки:**
До 10 попыток с экспоненциально растущим интервалом:
- 1-я попытка: через 60 секунд
- 2-я: через 150 секунд (×2.5)
- 3-я: через 375 секунд
- и так далее

Если в течение **8 часов** не получен успешный ответ — бот автоматически отписывается от вебхука.

### Long Polling (разработка)

Вы опрашиваете `GET /updates` — сервер удерживает соединение до появления событий или истечения тайм-аута. Каждое обновление имеет порядковый номер; параметр `marker` указывает на следующее ожидаемое.

---

## Клавиатура (inline-keyboard)

Inline-клавиатура размещается под сообщением бота. Ограничения:

- До **210 кнопок** всего.
- До **30 рядов**.
- До **7 кнопок в ряду** (до **3**, если это `link`, `open_app`, `request_geo_location` или `request_contact`).
- Ширина кнопок в одном ряду одинаковая; высота у всех кнопок одинаковая.
- Текст кнопки обрезается, если выходит за границы.
- Максимальная длина URL для кнопки `link` — **2048 символов**.

### Типы кнопок

| Тип                      | Поведение                                                                   |
| ------------------------ | --------------------------------------------------------------------------- |
| `callback`               | Сервер отправляет боту событие `message_callback` (через Webhook / Polling) |
| `link`                   | Открывает ссылку в новой вкладке                                            |
| `request_contact`        | Запрашивает у пользователя его контакт и телефон                            |
| `request_geo_location`   | Запрашивает местоположение                                                  |
| `open_app`               | Открывает мини-приложение                                                   |
| `message`                | Отправляет боту текстовое сообщение                                         |
| `clipboard`              | Копирует `payload` в буфер обмена                                           |

### Пример: добавление клавиатуры к сообщению

```json
{
  "text": "It is message with inline keyboard",
  "attachments": [
    {
      "type": "inline_keyboard",
      "payload": {
        "buttons": [
          [
            {
              "type": "callback",
              "text": "Press me!",
              "payload": "button1 pressed"
            }
          ]
        ]
      }
    }
  ]
}
```

### Пример: кнопка clipboard

```json
{
  "type": "clipboard",
  "text": "Скопировать",
  "payload": "123456"
}
```

---

## Форматирование текста

Чтобы включить разбор разметки, установите `format` в теле сообщения ([`NewMessageBody`](#newmessagebody)) в `"markdown"` или `"html"`.

### Markdown

| Эффект            | Синтаксис                                   |
| ----------------- | ------------------------------------------- |
| курсив            | `*text*` или `_text_`                       |
| жирный            | `**text**` или `__text__`                   |
| зачёркнутый       | `~~text~~`                                  |
| подчёркнутый      | `++text++`                                  |
| моноширинный      | `` `code` `` (переводы строк → пробелы)     |
| ссылка            | `[Docs](https://dev.max.ru/)`               |
| упоминание юзера  | `[Имя Фамилия](max://user/user_id)`         |

### HTML

| Эффект            | Теги                             |
| ----------------- | -------------------------------- |
| курсив            | `<i>` или `<em>`                 |
| жирный            | `<b>` или `<strong>`             |
| зачёркнутый       | `<del>` или `<s>`                |
| подчёркнутый      | `<ins>` или `<u>`                |
| моноширинный      | `<pre>` или `<code>`             |
| ссылка            | `<a href="https://dev.max.ru">Docs</a>` |
| упоминание юзера  | `<a href="max://user/user_id">Имя Фамилия</a>` |

> В упоминаниях указывайте полное имя пользователя из профиля MAX, включая фамилию (если она есть).

---

# Методы API

Все примеры используют cURL. Базовый URL — `https://platform-api.max.ru`. Везде подразумевается заголовок `Authorization: {access_token}`.

## bots

### GET `/me` — Получение информации о боте

Возвращает информацию о текущем боте, идентифицируемом по токену. Возвращает объект `BotInfo` (наследник [`User`](#user)) с ID, именем, никнеймом, описанием, аватаром и командами.

**Пример:**
```bash
curl -X GET "https://platform-api.max.ru/me" \
  -H "Authorization: {access_token}"
```

**Результат** (поля):

| Поле                 | Тип              | Описание                                                        |
| -------------------- | ---------------- | --------------------------------------------------------------- |
| `user_id`            | int64            | ID пользователя или бота                                        |
| `first_name`         | string           | Отображаемое имя                                                |
| `last_name`          | string, nullable | Фамилия (для ботов не возвращается)                             |
| `username`           | string, nullable | Никнейм                                                         |
| `is_bot`             | boolean          | `true`, если это бот                                            |
| `last_activity_time` | int64            | Последняя активность (Unix ms)                                  |
| `name`               | string, nullable | **Устаревшее**, скоро будет удалено                             |
| `description`        | string, nullable | До 16 000 символов                                              |
| `avatar_url`         | string           | URL уменьшенного аватара                                        |
| `full_avatar_url`    | string           | URL полного аватара                                             |
| `commands`           | `BotCommand[]`, nullable | До 32 команд, поддерживаемых ботом                      |

---

## chats

### GET `/chats` — Получение списка всех групповых чатов

Возвращает список чатов, в которых участвовал бот, с пагинацией.

**Пример:**
```bash
curl -X GET "https://platform-api.max.ru/chats" \
  -H "Authorization: {access_token}"
```

**Query-параметры:**

| Параметр | Тип      | Описание                                         |
| -------- | -------- | ------------------------------------------------ |
| `count`  | int, 1–100, default `50` | Сколько чатов вернуть            |
| `marker` | int64, optional          | Указатель на следующую страницу. Для первой — `null` |

**Результат:**

| Поле     | Тип             | Описание                                |
| -------- | --------------- | --------------------------------------- |
| `chats`  | [`Chat[]`](#chat) | Список чатов                           |
| `marker` | int64, nullable | Указатель на следующую страницу         |

---

### GET `/chats/{chatId}` — Получение информации о групповом чате

**Пример:**
```bash
curl -X GET "https://platform-api.max.ru/chats/{chatId}" \
  -H "Authorization: {access_token}"
```

**Параметры пути:** `chatId` — int64, ID запрашиваемого чата.

**Результат:** объект [`Chat`](#chat) (см. раздел «Объекты»).

---

### PATCH `/chats/{chatId}` — Изменение информации о групповом чате

Позволяет редактировать название, иконку, закреплённое сообщение.

**Пример:**
```bash
curl -X PATCH "https://platform-api.max.ru/chats/{chatId}" \
  -H "Authorization: {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "icon": { "url": "https://example.com/image.jpg" },
    "title": "Название чата",
    "notify": true
  }'
```

**Параметры пути:** `chatId` — int64.

**Тело запроса:**

| Поле     | Тип                                     | Описание                                  |
| -------- | --------------------------------------- | ----------------------------------------- |
| `icon`   | `PhotoAttachmentRequestPayload`, nullable | Изображение (поля взаимоисключающие)    |
| `title`  | string, nullable, 1–200 символов        | Новое название                            |
| `pin`    | string, nullable                        | ID сообщения, которое закрепить           |
| `notify` | boolean, default `true`                 | Уведомлять ли участников об изменении     |

**Результат:** обновлённый объект [`Chat`](#chat).

---

### DELETE `/chats/{chatId}` — Удаление группового чата

Удаляет чат для всех участников.

**Пример:**
```bash
curl -X DELETE "https://platform-api.max.ru/chats/{chatId}" \
  -H "Authorization: {access_token}"
```

**Параметры:** `chatId` — int64.
**Результат:** `{ success, message }`.

---

### POST `/chats/{chatId}/actions` — Отправка действия бота в чат

Отображает пользователям индикаторы «печатает», «отправляет фото» и т. п.

**Пример:**
```bash
curl -X POST "https://platform-api.max.ru/chats/{chatId}/actions" \
  -H "Authorization: {access_token}" \
  -H "Content-Type: application/json" \
  -d '{ "action": "typing_on" }'
```

**Тело запроса:**

| Поле     | Тип  | Значения                                                                                    |
| -------- | ---- | ------------------------------------------------------------------------------------------- |
| `action` | enum | `typing_on`, `sending_photo`, `sending_video`, `sending_audio`, `sending_file`, `mark_seen` |

**Результат:** `{ success, message }`.

---

### GET `/chats/{chatId}/pin` — Получение закреплённого сообщения

**Пример:**
```bash
curl -X GET "https://platform-api.max.ru/chats/{chatId}/pin" \
  -H "Authorization: {access_token}"
```

**Результат:**

| Поле      | Тип                      | Описание                                     |
| --------- | ------------------------ | -------------------------------------------- |
| `message` | [`Message`](#message), nullable | Закреплённое сообщение или `null`       |

---

### PUT `/chats/{chatId}/pin` — Закрепление сообщения

**Пример:**
```bash
curl -X PUT "https://platform-api.max.ru/chats/{chatId}/pin" \
  -H "Authorization: {access_token}" \
  -H "Content-Type: application/json" \
  -d '{ "message_id": "{message_id}", "notify": true }'
```

**Тело запроса:**

| Поле         | Тип                     | Описание                                      |
| ------------ | ----------------------- | --------------------------------------------- |
| `message_id` | string                  | ID сообщения (соответствует `Message.body.mid`) |
| `notify`     | boolean, default `true` | Отправлять ли системное уведомление           |

**Результат:** `{ success, message }`.

---

### DELETE `/chats/{chatId}/pin` — Удаление закреплённого сообщения

```bash
curl -X DELETE "https://platform-api.max.ru/chats/{chatId}/pin" \
  -H "Authorization: {access_token}"
```

**Результат:** `{ success, message }`.

---

### GET `/chats/{chatId}/members/me` — Информация о членстве бота в чате

Возвращает объект `ChatMember` (наследник [`User`](#user)) с правами бота в данном чате.

**Пример:**
```bash
curl -X GET "https://platform-api.max.ru/chats/{chatId}/members/me" \
  -H "Authorization: {access_token}"
```

**Дополнительные поля результата (помимо полей `User`):**

| Поле               | Тип                        | Описание                                                                 |
| ------------------ | -------------------------- | ------------------------------------------------------------------------ |
| `last_access_time` | int64                      | Последняя активность в чате (может быть устаревшей для суперчатов)       |
| `is_owner`         | boolean                    | Владелец ли чата                                                         |
| `is_admin`         | boolean                    | Администратор ли чата                                                    |
| `join_time`        | int64                      | Дата вступления (Unix time)                                              |
| `permissions`      | `ChatAdminPermission[]`, nullable | Список прав                                                       |
| `alias`            | string                     | Заголовок (например, «владелец», «админ»)                                |

**Возможные значения `permissions`:**

- `read_all_messages` — читать все сообщения
- `add_remove_members` — добавлять/удалять участников
- `add_admins` — добавлять администраторов
- `change_chat_info` — изменять информацию о чате
- `pin_message` — закреплять сообщения
- `write` — писать сообщения
- `can_call` — совершать звонки
- `edit_link` — изменять ссылку на чат
- `post_edit_delete_message` — публиковать/редактировать/удалять сообщения
- `edit_message` — редактировать сообщения
- `delete_message` — удалять сообщения

---

### DELETE `/chats/{chatId}/members/me` — Удаление бота из чата

Бот покидает чат.

```bash
curl -X DELETE "https://platform-api.max.ru/chats/{chatId}/members/me" \
  -H "Authorization: {access_token}"
```

**Результат:** `{ success, message }`.

---

### GET `/chats/{chatId}/members/admins` — Список администраторов

Бот должен быть администратором.

```bash
curl -X GET "https://platform-api.max.ru/chats/{chatId}/members/admins" \
  -H "Authorization: {access_token}"
```

**Результат:**

| Поле      | Тип             | Описание                                  |
| --------- | --------------- | ----------------------------------------- |
| `members` | `ChatMember[]`  | Список администраторов                    |
| `marker`  | int64, nullable | Указатель на следующую страницу           |

---

### POST `/chats/{chatId}/members/admins` — Назначить администратора

**Пример:**
```bash
curl -X POST "https://platform-api.max.ru/chats/{chatId}/members/admins" \
  -H "Authorization: {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "admins": [
      {
        "user_id": "{user_id}",
        "permissions": [
          "read_all_messages",
          "add_remove_members",
          "add_admins",
          "change_chat_info",
          "pin_message",
          "write"
        ],
        "alias": "Admin"
      }
    ]
  }'
```

**Тело запроса:**

| Поле     | Тип             | Описание                                     |
| -------- | --------------- | -------------------------------------------- |
| `admins` | `ChatAdmin[]`   | Список пользователей для назначения админами |
| `marker` | int64, nullable | Указатель на следующую страницу              |

**Результат:** `{ success, message }`.

---

### DELETE `/chats/{chatId}/members/admins/{userId}` — Отмена прав администратора

```bash
curl -X DELETE "https://platform-api.max.ru/chats/{chatId}/members/admins/{userId}" \
  -H "Authorization: {access_token}"
```

**Параметры пути:**

| Параметр | Тип   | Описание             |
| -------- | ----- | -------------------- |
| `chatId` | int64 | ID чата              |
| `userId` | int64 | ID пользователя      |

**Результат:** `{ success, message }`.

---

### GET `/chats/{chatId}/members` — Получение участников чата

**Пример:**
```bash
curl -X GET "https://platform-api.max.ru/chats/{chatId}/members" \
  -H "Authorization: {access_token}"
```

**Query-параметры:**

| Параметр   | Тип                 | Описание                                                                            |
| ---------- | ------------------- | ----------------------------------------------------------------------------------- |
| `user_ids` | int[], nullable     | Список конкретных пользователей. Если указан — `count` и `marker` игнорируются.     |
| `marker`   | int64, optional     | Указатель на следующую страницу                                                     |
| `count`    | int, 1–100, def. 20 | Количество участников                                                               |

**Результат:**

| Поле      | Тип             | Описание                        |
| --------- | --------------- | ------------------------------- |
| `members` | `ChatMember[]`  | Список участников               |
| `marker`  | int64, nullable | Указатель на следующую страницу |

---

### POST `/chats/{chatId}/members` — Добавление участников

**Пример:**
```bash
curl -X POST "https://platform-api.max.ru/chats/{chatId}/members" \
  -H "Authorization: {access_token}" \
  -H "Content-Type: application/json" \
  -d '{ "user_ids": ["{user_id_1}", "{user_id_2}"] }'
```

**Тело запроса:**

| Поле       | Тип     | Описание                         |
| ---------- | ------- | -------------------------------- |
| `user_ids` | int64[] | ID пользователей для добавления |

**Результат:**

| Поле                  | Тип                       | Описание                                          |
| --------------------- | ------------------------- | ------------------------------------------------- |
| `success`             | boolean                   |                                                   |
| `message`             | string                    | Опциональное пояснение                            |
| `failed_user_ids`     | int64[], nullable         | Не добавленные ID                                 |
| `failed_user_details` | `FailedUserDetails[]`, nullable | Подробности по каждому неудачному добавлению |

---

### DELETE `/chats/{chatId}/members` — Удаление участника

```bash
curl -X DELETE "https://platform-api.max.ru/chats/{chatId}/members?user_id={user_id}&block=true" \
  -H "Authorization: {access_token}"
```

**Query-параметры:**

| Параметр  | Тип     | Описание                                                                                 |
| --------- | ------- | ---------------------------------------------------------------------------------------- |
| `user_id` | int64   | ID удаляемого пользователя                                                               |
| `block`   | boolean | Если `true` — заблокировать пользователя (только для чатов с публичной/приватной ссылкой) |

**Результат:** `{ success, message }`.

---

## subscriptions

### GET `/subscriptions` — Получение подписок

Возвращает список всех Webhook-подписок бота.

```bash
curl -X GET "https://platform-api.max.ru/subscriptions" \
  -H "Authorization: {access_token}"
```

**Результат:**

| Поле            | Тип               | Описание                    |
| --------------- | ----------------- | --------------------------- |
| `subscriptions` | `Subscription[]`  | Список текущих подписок     |

---

### POST `/subscriptions` — Подписка на обновления

Настраивает Webhook-доставку событий. При активной подписке Long Polling (`GET /updates`) не работает.

**Модель доставки:**

1. При наступлении события MAX вызывает ваш Webhook-endpoint.
2. Проводится TLS-валидация endpoint'а.
3. Отправляется HTTP POST с телом в виде [`Update`](#update).
4. Если при создании подписки задан `secret` — MAX передаёт его в заголовке `X-Max-Bot-Api-Secret`.
5. Endpoint должен ответить **HTTP 200 в течение 30 секунд**.

**Требования к Webhook-endpoint:**

- Протокол: **HTTPS**, порт **443** (в URL не указывается).
- Валидный TLS-сертификат от доверенного CA.
- Домен URL совпадает с CN/SAN сертификата.
- Сервер отдаёт полную цепочку сертификатов.

**Пример:**
```bash
curl -X POST "https://platform-api.max.ru/subscriptions" \
  -H "Authorization: {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-domain.com/webhook",
    "update_types": ["message_created", "bot_started"],
    "secret": "your_secret"
  }'
```

**Тело запроса:**

| Поле           | Тип       | Описание                                                                                            |
| -------------- | --------- | --------------------------------------------------------------------------------------------------- |
| `url`          | string    | HTTPS URL, обязательно начинается с `https://`                                                      |
| `update_types` | string[], optional | Список типов событий, которые нужно получать                                               |
| `secret`       | string, optional, 5–256 символов, `^[a-zA-Z0-9_-]+$` | Секрет для заголовка `X-Max-Bot-Api-Secret` |

**Политика ретраев:** до 10 попыток, интервалы ×2.5 (60 с → 150 с → 375 с → …). После **8 часов** неуспехов бот автоматически отписывается.

**Безопасность:** обязательно проверяйте заголовок `X-Max-Bot-Api-Secret`, если задавали `secret` — это защищает от подделки запросов третьими лицами.

**Результат:** `{ success, message }`.

---

### DELETE `/subscriptions` — Отписка от обновлений

После отписки снова становится доступен Long Polling.

```bash
curl -X DELETE "https://platform-api.max.ru/subscriptions?url=https://your-domain.com/webhook" \
  -H "Authorization: {access_token}"
```

**Query-параметры:**

| Параметр | Тип    | Описание                                    |
| -------- | ------ | ------------------------------------------- |
| `url`    | string | URL, который нужно удалить из подписок      |

**Результат:** `{ success, message }`.

---

### GET `/updates` — Получение обновлений (Long Polling)

Используется для разработки и тестирования, если Webhook не настроен. Каждый `Update` имеет порядковый номер; `marker` указывает на следующий ожидаемый. Если `marker` не передан — получаете все обновления после последнего подтверждения.

```bash
curl -X GET "https://platform-api.max.ru/updates" \
  -H "Authorization: {access_token}"
```

**Query-параметры:**

| Параметр  | Тип                                | Описание                                     |
| --------- | ---------------------------------- | -------------------------------------------- |
| `limit`   | int, 1–1000, default `100`         | Максимум обновлений за раз                   |
| `timeout` | int, 0–90, default `30`            | Тайм-аут long poll в секундах                |
| `marker`  | int64, nullable                    | Если передан — получаете ещё не полученные   |
| `types`   | string[], nullable                 | Фильтр по типам (`message_created` и т. д.) |

**Результат:**

| Поле      | Тип                       | Описание                        |
| --------- | ------------------------- | ------------------------------- |
| `updates` | [`Update[]`](#update)     | Страница обновлений             |
| `marker`  | int64, nullable           | Указатель на следующую страницу |

---

## upload

### POST `/uploads` — Загрузка файлов

Возвращает URL для последующей загрузки файла. Загрузка медиа в MAX — двухэтапный процесс.

> ⚠️ Параметр `type=photo` больше не поддерживается — замените на `type=image`.

**Два способа загрузки:**

1. **Multipart upload** (проще, но менее надёжен) — `Content-Type: multipart/form-data`. Файл отправляется целиком; при обрыве — заново.
2. **Resumable upload** — если `Content-Type` не равен `multipart/form-data`. Можно загружать частями и возобновлять.

**Общие ограничения:**
- Максимальный размер файла: **4 ГБ**.
- Можно загружать только **один файл за раз**.

**Query-параметры:**

| Параметр | Значения                          | Описание                                                                                 |
| -------- | --------------------------------- | ---------------------------------------------------------------------------------------- |
| `type`   | `image` / `video` / `audio` / `file` | Тип файла                                                                             |

**Поддерживаемые форматы:**

| Тип     | Форматы                                  |
| ------- | ---------------------------------------- |
| `image` | JPG, JPEG, PNG, GIF, TIFF, BMP, HEIC     |
| `video` | MP4, MOV, MKV, WEBM, MATROSKA            |
| `audio` | MP3, WAV, M4A и другие                   |
| `file`  | любые форматы                            |

**Результат:**

| Поле    | Тип    | Описание                                                           |
| ------- | ------ | ------------------------------------------------------------------ |
| `url`   | string | URL для загрузки файла (срок жизни не ограничен)                   |
| `token` | string, optional | Токен видео или аудио (для `video`/`audio`)              |

---

#### Пошаговый процесс: image или file

1. Получите URL:
```bash
curl -X POST "https://platform-api.max.ru/uploads?type=file" \
  -H "Authorization: {access_token}"
```

2. Загрузите файл по URL:
```bash
curl -i -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "data=@movie.pdf" "%UPLOAD_URL%"
```

3. В ответе получите JSON-объект с `token`. Используйте его в `attachments`:
```json
{
  "type": "file",
  "payload": { "token": "<полученный_token>" }
}
```

#### Пошаговый процесс: video или audio

Для видео и аудио **`token` приходит уже на первом шаге** (вместе с `url`).

1. Получите URL и token:
```bash
curl -X POST "https://platform-api.max.ru/uploads?type=video" \
  -H "Authorization: {access_token}"
```

Ответ:
```json
{ "url": "https://vu.mycdn.me/upload.do…", "token": "..." }
```

2. Загрузите файл:
```bash
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "data=@movie.mp4" \
  "https://vu.mycdn.me/upload.do?sig={signature}&expires={timestamp}"
```

Сервер вернёт `retval`. После этого `token` становится активным.

3. Отправьте сообщение:
```json
{
  "text": "Message with video",
  "attachments": [
    {
      "type": "video",
      "payload": { "token": "_3Rarhcf1PtlMXy8jpgie8Ai_KARnVFYNQTtmIRWNh4" }
    }
  ]
}
```

#### Обработка файлов и типичная ошибка

После загрузки сервер обрабатывает файл (крупные файлы — дольше). Если отправить сообщение сразу после загрузки, можно получить:
```json
{
  "code": "attachment.not.ready",
  "message": "Key: errors.process.attachment.file.not.processed"
}
```

**Рекомендации:**
- Делайте паузу перед отправкой сообщения.
- При неудаче повторяйте с **экспоненциально растущим** интервалом.
- Часто используемые файлы загружайте заранее и переиспользуйте токен.

---

## messages

### GET `/messages` — Получение сообщений

Возвращает сообщения из чата или по списку ID. Обязателен **один** из параметров: `chat_id` или `message_ids`.

Сообщения возвращаются в **обратном порядке** (новые первыми), если запрос по `chat_id`.

**Примеры:**
```bash
# По чату
curl -X GET "https://platform-api.max.ru/messages?chat_id={chat_id}" \
  -H "Authorization: {access_token}"

# По списку ID
curl -X GET "https://platform-api.max.ru/messages?message_ids={message_id1},{message_id2}" \
  -H "Authorization: {access_token}"
```

**Query-параметры:**

| Параметр      | Тип                          | Описание                                                      |
| ------------- | ---------------------------- | ------------------------------------------------------------- |
| `chat_id`     | int64, optional              | ID чата. Обязателен, если не задан `message_ids`              |
| `message_ids` | list/csv, optional           | Список ID сообщений. Обязателен, если не задан `chat_id`      |
| `from`        | int64, optional              | Начало диапазона (Unix timestamp)                             |
| `to`          | int64, optional              | Конец диапазона                                               |
| `count`       | int, 1–100, default `50`     | Максимум сообщений                                            |

**Результат:**

| Поле       | Тип                     | Описание            |
| ---------- | ----------------------- | ------------------- |
| `messages` | [`Message[]`](#message) | Массив сообщений    |

---

### POST `/messages` — Отправить сообщение

Нужно указать **одного** получателя: `user_id` (личка) **или** `chat_id` (чат).

**Пример:**
```bash
curl -X POST "https://platform-api.max.ru/messages?user_id={user_id}" \
  -H "Authorization: {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Это сообщение с кнопкой-ссылкой",
    "attachments": [
      {
        "type": "inline_keyboard",
        "payload": {
          "buttons": [
            [
              { "type": "link", "text": "Откройте сайт", "url": "https://example.com" }
            ]
          ]
        }
      }
    ]
  }'
```

**Query-параметры:**

| Параметр                | Тип     | Описание                                                                    |
| ----------------------- | ------- | --------------------------------------------------------------------------- |
| `user_id`               | int64, optional | ID пользователя (для отправки в личку)                              |
| `chat_id`               | int64, optional | ID чата (для отправки в чат)                                        |
| `disable_link_preview`  | boolean, optional | Если `false`, сервер **не генерирует** превью для ссылок          |

**Тело запроса** — объект [`NewMessageBody`](#newmessagebody):

| Поле          | Тип                                     | Описание                              |
| ------------- | --------------------------------------- | ------------------------------------- |
| `text`        | string, nullable, до 4000 символов      | Текст сообщения                       |
| `attachments` | `AttachmentRequest[]`, nullable         | Вложения                              |
| `link`        | `NewMessageLink`, nullable              | Ссылка на сообщение (reply / forward) |
| `notify`      | boolean, optional, default `true`       | Уведомлять ли участников              |
| `format`      | enum `"markdown"` / `"html"`, nullable  | Форматирование текста                 |

**Результат:**

| Поле      | Тип                  | Описание              |
| --------- | -------------------- | --------------------- |
| `message` | [`Message`](#message) | Созданное сообщение   |

---

### PUT `/messages` — Редактировать сообщение

> Можно редактировать только сообщения **не старше 24 часов**.

Если `attachments` равен `null` — вложения не меняются. Если передан пустой список — все вложения удаляются.

**Пример:**
```bash
curl -X PUT "https://platform-api.max.ru/messages?message_id=message_id" \
  -H "Authorization: {access_token}" \
  -H "Content-Type: application/json" \
  -d '{ "text": "Изменённый текст" }'
```

**Query-параметры:** `message_id` (string, ≥ 1 символа) — ID редактируемого сообщения.

**Тело запроса:** такой же [`NewMessageBody`](#newmessagebody), как в `POST /messages`.

**Результат:** `{ success, message }`.

---

### DELETE `/messages` — Удалить сообщение

> Можно удалять только сообщения **не старше 24 часов**. Бот должен иметь разрешение на удаление.

```bash
curl -X DELETE "https://platform-api.max.ru/messages?message_id={message_id}" \
  -H "Authorization: {access_token}"
```

**Query-параметры:** `message_id` — string, ≥ 1 символа.
**Результат:** `{ success, message }`.

---

### GET `/messages/{messageId}` — Получение одного сообщения

```bash
curl -X GET "https://platform-api.max.ru/messages/{messageId}" \
  -H "Authorization: {access_token}"
```

**Параметры пути:** `messageId` — string, pattern `[a-zA-Z0-9_\-]+` (это значение `mid`).

**Результат:** объект [`Message`](#message).

---

### GET `/videos/{videoToken}` — Получить информацию о видео

Возвращает URL-адреса воспроизведения и метаданные прикреплённого видео.

```bash
curl -X GET "https://platform-api.max.ru/videos/{video_token}" \
  -H "Authorization: {access_token}"
```

**Параметры пути:** `videoToken` — string.

**Результат:**

| Поле         | Тип                              | Описание                                                  |
| ------------ | -------------------------------- | --------------------------------------------------------- |
| `token`      | string                           | Токен видео-вложения                                      |
| `urls`       | `VideoUrls`, nullable            | URL'ы для скачивания/воспроизведения (null если недоступно)|
| `thumbnail`  | `PhotoAttachmentPayload`, nullable | Миниатюра                                              |
| `width`      | int                              | Ширина                                                    |
| `height`     | int                              | Высота                                                    |
| `duration`   | int                              | Длительность в секундах                                   |

---

## answers

### POST `/answers` — Ответ на callback

Используется после нажатия на callback-кнопку. Можно либо обновить текущее сообщение, либо показать одноразовое уведомление пользователю (либо то и другое).

**Пример:**
```bash
curl -X POST "https://platform-api.max.ru/answers?callback_id=callback_id" \
  -H "Authorization: {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "text": "Это сообщение с кнопкой-ссылкой",
      "attachments": [
        {
          "type": "inline_keyboard",
          "payload": {
            "buttons": [
              [ { "type": "link", "text": "Откройте сайт", "url": "https://example.com" } ]
            ]
          }
        }
      ]
    }
  }'
```

**Query-параметры:**

| Параметр      | Тип    | Описание                                                                                                      |
| ------------- | ------ | ------------------------------------------------------------------------------------------------------------- |
| `callback_id` | string | ID нажатой кнопки. Приходит в `Update` с типом `message_callback`, поле `updates[i].callback.callback_id`    |

**Тело запроса:**

| Поле           | Тип                                  | Описание                                        |
| -------------- | ------------------------------------ | ----------------------------------------------- |
| `message`      | [`NewMessageBody`](#newmessagebody), nullable | Если надо изменить текущее сообщение     |
| `notification` | string, nullable                     | Если надо показать одноразовое уведомление      |

**Результат:** `{ success, message }`.

---

# Объекты

## User

Базовый объект пользователя/бота. Имеет несколько наследников:

- **`User`** — общая информация без аватара.
- **`UserWithPhoto`** — то же + `avatar_url`, `full_avatar_url`, `description`.
- **`BotInfo`** — `UserWithPhoto` + `commands`; возвращается только из `GET /me`.
- **`ChatMember`** — `UserWithPhoto` + членская информация (`is_owner`, `is_admin`, `permissions`, `join_time`, `last_access_time`, `alias`); возвращается методами `/chats/.../members/...`.

**Поля `User`:**

| Поле                 | Тип               | Описание                                                                               |
| -------------------- | ----------------- | -------------------------------------------------------------------------------------- |
| `user_id`            | int64             | Идентификатор                                                                          |
| `first_name`         | string            | Отображаемое имя                                                                       |
| `last_name`          | string, nullable  | Фамилия (ботам не возвращается)                                                        |
| `username`           | string, nullable  | Никнейм или публичное имя. Может быть `null`, если не задано                           |
| `is_bot`             | boolean           | `true` для бота                                                                        |
| `last_activity_time` | int64             | Unix ms. Может не возвращаться, если пользователь скрыл онлайн-статус                  |
| `name`               | string, nullable  | **Устаревшее**, будет удалено                                                          |

**Пример:**
```json
{
  "user_id": 0,
  "first_name": "string",
  "last_name": "string",
  "username": "string",
  "is_bot": true,
  "last_activity_time": 0,
  "name": "string"
}
```

---

## Chat

Групповой чат или диалог.

| Поле                | Тип                              | Описание                                                                                      |
| ------------------- | -------------------------------- | --------------------------------------------------------------------------------------------- |
| `chat_id`           | int64                            | ID чата                                                                                       |
| `type`              | enum `"chat"`                    | Тип (пока единственное значение)                                                              |
| `status`            | enum                             | `active` / `removed` / `left` / `closed` — статус бота в чате                                 |
| `title`             | string, nullable                 | Название. `null` для диалогов                                                                 |
| `icon`              | `Image`, nullable                | Иконка чата                                                                                   |
| `last_event_time`   | int64                            | Время последнего события                                                                      |
| `participants_count`| int32                            | Число участников. Для диалогов всегда `2`                                                     |
| `owner_id`          | int64, nullable                  | ID владельца                                                                                  |
| `participants`      | object, nullable                 | Участники с временем последней активности. `null`, если запрашивается список чатов            |
| `is_public`         | boolean                          | Публичный ли чат. Для диалогов всегда `false`                                                 |
| `link`              | string, nullable                 | Ссылка на чат                                                                                 |
| `description`       | string, nullable                 | Описание                                                                                      |
| `dialog_with_user`  | `UserWithPhoto`, nullable        | Только для `"dialog"`                                                                         |
| `chat_message_id`   | string, nullable                 | ID сообщения, чья кнопка инициировала чат                                                     |
| `pinned_message`    | [`Message`](#message), nullable  | Закреплённое сообщение (возвращается только при запросе конкретного чата)                     |

**Значения `status`:**
- `active` — бот активный участник
- `removed` — бот удалён
- `left` — бот покинул чат
- `closed` — чат закрыт

**Пример:**
```json
{
  "chat_id": 0,
  "type": "chat",
  "status": "active",
  "title": "string",
  "icon": { },
  "last_event_time": 0,
  "participants_count": 0,
  "owner_id": 0,
  "participants": { },
  "is_public": true,
  "link": "string",
  "description": "string",
  "dialog_with_user": { },
  "chat_message_id": "string",
  "pinned_message": { }
}
```

---

## Message

Сообщение в чате.

| Поле        | Тип                             | Описание                                                                 |
| ----------- | ------------------------------- | ------------------------------------------------------------------------ |
| `sender`    | `User`, optional                | Отправитель                                                              |
| `recipient` | `Recipient`                     | Получатель (пользователь или чат)                                        |
| `timestamp` | int64                           | Время создания (Unix time)                                               |
| `link`      | `LinkedMessage`, nullable       | Пересланное или ответное сообщение                                       |
| `body`      | `MessageBody`                   | Содержимое (текст + вложения). `null`, если сообщение только пересланное |
| `stat`      | `MessageStat`, nullable         | Статистика (только для постов в каналах)                                 |
| `url`       | string, nullable                | Публичная ссылка (только для постов в каналах)                           |

`MessageBody` обычно содержит поле `mid` (ID сообщения), `seq`, `text`, `attachments`.

**Пример:**
```json
{
  "sender": { },
  "recipient": { },
  "timestamp": 0,
  "link": { },
  "body": { },
  "stat": { },
  "url": "string"
}
```

---

## NewMessageBody

Тело запроса для создания/редактирования сообщения.

| Поле          | Тип                                    | Описание                                              |
| ------------- | -------------------------------------- | ----------------------------------------------------- |
| `text`        | string, nullable, до 4000 символов     | Текст                                                 |
| `attachments` | `AttachmentRequest[]`, nullable        | Вложения. Пустой массив = удалить все вложения        |
| `link`        | `NewMessageLink`, nullable             | Ссылка на сообщение (для reply/forward)               |
| `notify`      | boolean, optional, default `true`      | Уведомлять ли участников                              |
| `format`      | enum `"markdown"` / `"html"`, nullable | Формат разметки                                       |

**Пример:**
```json
{
  "text": "string",
  "attachments": [ { } ],
  "link": { },
  "notify": true,
  "format": "markdown"
}
```

---

## Update

Объект входящего события. Реальные события различаются полем `update_type` и дополнительными полями в зависимости от типа.

> Чтобы получать события из группового чата или канала, назначьте бота администратором.

**Общие поля (присутствуют во всех типах):**

| Поле          | Тип                   | Описание                                              |
| ------------- | --------------------- | ----------------------------------------------------- |
| `update_type` | string                | Тип события                                           |
| `timestamp`   | int64                 | Unix-время наступления события (мс)                   |

**Типы событий** (значения `update_type`):

### `message_created` — создано новое сообщение

| Поле          | Тип                   | Описание                                    |
| ------------- | --------------------- | ------------------------------------------- |
| `message`     | [`Message`](#message) | Новое сообщение                             |
| `user_locale` | string, nullable      | Язык пользователя (IETF BCP 47), только в диалогах |

### `message_callback` — нажата callback-кнопка

| Поле          | Тип                       | Описание                                    |
| ------------- | ------------------------- | ------------------------------------------- |
| `callback`    | `Callback`                | Информация о нажатии кнопки                 |
| `message`     | [`Message`](#message)     | Сообщение, к которому прикреплена кнопка    |
| `user_locale` | string, nullable          | Язык пользователя                           |

`Callback` содержит:

| Поле           | Тип              | Описание                                |
| -------------- | ---------------- | --------------------------------------- |
| `callback_id`  | string           | ID callback-запроса                     |
| `timestamp`    | int64            | Время нажатия (Unix ms)                 |
| `user`         | [`User`](#user)  | Пользователь, нажавший кнопку          |
| `payload`      | string, nullable | Данные из `payload` кнопки             |
| `message`      | [`Message`](#message), nullable | Сообщение (может быть null)  |

### `message_edited` — сообщение отредактировано

| Поле          | Тип                   | Описание                                    |
| ------------- | --------------------- | ------------------------------------------- |
| `message`     | [`Message`](#message) | Отредактированное сообщение                 |

### `message_removed` — сообщение удалено

| Поле          | Тип                   | Описание                                    |
| ------------- | --------------------- | ------------------------------------------- |
| `message_id`  | string                | ID удалённого сообщения                     |
| `chat_id`     | int64                 | ID чата                                     |
| `user_id`     | int64                 | ID пользователя, удалившего сообщение       |

### `bot_started` — пользователь запустил бота

| Поле          | Тип                  | Описание                                     |
| ------------- | -------------------- | -------------------------------------------- |
| `chat_id`     | int64                | ID диалога                                   |
| `user`        | [`User`](#user)      | Пользователь, нажавший кнопку «Start»        |
| `payload`     | string, nullable     | Deep link payload (до 512 символов)          |
| `user_locale` | string, optional     | Язык пользователя (IETF BCP 47)             |

### `bot_stopped` — пользователь остановил бота

| Поле          | Тип                  | Описание                                     |
| ------------- | -------------------- | -------------------------------------------- |
| `chat_id`     | int64                | ID диалога                                   |
| `user`        | [`User`](#user)      | Пользователь, остановивший бота              |
| `user_locale` | string               | Язык пользователя (IETF BCP 47)             |

### `bot_added` — бот добавлен в чат

| Поле          | Тип                  | Описание                                     |
| ------------- | -------------------- | -------------------------------------------- |
| `chat_id`     | int64                | ID чата                                      |
| `user`        | [`User`](#user)      | Пользователь, добавивший бота                |
| `is_channel`  | boolean              | Добавлен в канал или нет                     |

### `bot_removed` — бот удалён из чата

| Поле          | Тип                  | Описание                                     |
| ------------- | -------------------- | -------------------------------------------- |
| `chat_id`     | int64                | ID чата                                      |
| `user`        | [`User`](#user)      | Пользователь, удаливший бота                 |
| `is_channel`  | boolean              | Удалён из канала или нет                     |

### `user_added` — пользователь добавлен в чат

| Поле          | Тип                  | Описание                                     |
| ------------- | -------------------- | -------------------------------------------- |
| `chat_id`     | int64                | ID чата                                      |
| `user`        | [`User`](#user)      | Добавленный пользователь                     |
| `inviter_id`  | int64, nullable      | ID пригласившего (null если вошёл по ссылке)  |
| `is_channel`  | boolean              | Добавлен в канал или нет                     |

### `user_removed` — пользователь удалён из чата

| Поле          | Тип                  | Описание                                     |
| ------------- | -------------------- | -------------------------------------------- |
| `chat_id`     | int64                | ID чата                                      |
| `user`        | [`User`](#user)      | Удалённый пользователь                       |
| `admin_id`    | int64, nullable      | Админ, удаливший (null если вышел сам)       |
| `is_channel`  | boolean              | Удалён из канала или нет                     |

### `chat_title_changed` — изменено название чата

| Поле          | Тип                  | Описание                                     |
| ------------- | -------------------- | -------------------------------------------- |
| `chat_id`     | int64                | ID чата                                      |
| `user`        | [`User`](#user)      | Пользователь, изменивший название            |
| `title`       | string               | Новое название чата                          |

### `dialog_muted` — уведомления диалога отключены

| Поле          | Тип                  | Описание                                     |
| ------------- | -------------------- | -------------------------------------------- |
| `chat_id`     | int64                | ID чата                                      |
| `user`        | [`User`](#user)      | Пользователь                                 |
| `muted_until` | int64                | Unix-время, до которого отключены уведомления |
| `user_locale` | string               | Язык пользователя                            |

### `dialog_unmuted` — уведомления диалога включены

| Поле          | Тип                  | Описание                                     |
| ------------- | -------------------- | -------------------------------------------- |
| `chat_id`     | int64                | ID чата                                      |
| `user`        | [`User`](#user)      | Пользователь                                 |
| `user_locale` | string               | Язык пользователя                            |

### `dialog_cleared` — диалог очищен

| Поле          | Тип                  | Описание                                     |
| ------------- | -------------------- | -------------------------------------------- |
| `chat_id`     | int64                | ID чата                                      |
| `user`        | [`User`](#user)      | Пользователь                                 |
| `user_locale` | string               | Язык пользователя                            |

### `dialog_removed` — диалог удалён

| Поле          | Тип                  | Описание                                     |
| ------------- | -------------------- | -------------------------------------------- |
| `chat_id`     | int64                | ID чата                                      |
| `user`        | [`User`](#user)      | Пользователь, удаливший чат                  |
| `user_locale` | string               | Язык пользователя                            |

**Пример (`message_created`):**
```json
{
  "update_type": "message_created",
  "timestamp": 1776090860108,
  "message": { ... },
  "user_locale": "ru"
}
```

**Пример (`message_callback`):**
```json
{
  "update_type": "message_callback",
  "timestamp": 1776090860108,
  "message": { ... },
  "callback": {
    "callback_id": "f9LHodD0cO...",
    "timestamp": 1776090860108,
    "user": { "user_id": 248173258, "first_name": "Michael" },
    "payload": "action:click"
  }
}
```

**Пример (`bot_started`):**
```json
{
  "update_type": "bot_started",
  "timestamp": 1776090860108,
  "chat_id": -73419880556746,
  "user": { "user_id": 248173258, "first_name": "Michael" },
  "payload": "deep_link_data"
}
```

---

# Сводная таблица всех методов

| Метод и путь                                          | Назначение                             |
| ----------------------------------------------------- | -------------------------------------- |
| `GET /me`                                             | Информация о боте                      |
| `GET /chats`                                          | Список групповых чатов                 |
| `GET /chats/{chatId}`                                 | Информация о чате                      |
| `PATCH /chats/{chatId}`                               | Изменить чат                           |
| `DELETE /chats/{chatId}`                              | Удалить чат                            |
| `POST /chats/{chatId}/actions`                        | Отправить действие (typing и т. п.)    |
| `GET /chats/{chatId}/pin`                             | Получить закреп. сообщение             |
| `PUT /chats/{chatId}/pin`                             | Закрепить сообщение                    |
| `DELETE /chats/{chatId}/pin`                          | Удалить закрепление                    |
| `GET /chats/{chatId}/members/me`                      | Членство бота в чате                   |
| `DELETE /chats/{chatId}/members/me`                   | Покинуть чат                           |
| `GET /chats/{chatId}/members/admins`                  | Список админов                         |
| `POST /chats/{chatId}/members/admins`                 | Назначить админов                      |
| `DELETE /chats/{chatId}/members/admins/{userId}`      | Снять права админа                     |
| `GET /chats/{chatId}/members`                         | Список участников                      |
| `POST /chats/{chatId}/members`                        | Добавить участников                    |
| `DELETE /chats/{chatId}/members`                      | Удалить участника                      |
| `GET /subscriptions`                                  | Список Webhook-подписок                |
| `POST /subscriptions`                                 | Подписка на Webhook                    |
| `DELETE /subscriptions`                               | Отписка от Webhook                     |
| `GET /updates`                                        | Получение обновлений (Long Polling)    |
| `POST /uploads`                                       | Получить URL для загрузки файла        |
| `GET /messages`                                       | Получить сообщения (список/по ID)      |
| `POST /messages`                                      | Отправить сообщение                    |
| `PUT /messages`                                       | Редактировать сообщение                |
| `DELETE /messages`                                    | Удалить сообщение                      |
| `GET /messages/{messageId}`                           | Получить одно сообщение                |
| `GET /videos/{videoToken}`                            | Информация о видео                     |
| `POST /answers`                                       | Ответ на callback                      |

---

# Краткие «рецепты»

### Отправка простого текстового сообщения в личку

```bash
curl -X POST "https://platform-api.max.ru/messages?user_id=12345" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "text": "Привет!" }'
```

### Отправка сообщения с inline-клавиатурой в чат

```bash
curl -X POST "https://platform-api.max.ru/messages?chat_id=-100500" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Нажми кнопку",
    "attachments": [{
      "type": "inline_keyboard",
      "payload": {
        "buttons": [[
          { "type": "callback", "text": "Жми", "payload": "btn_pressed" }
        ]]
      }
    }]
  }'
```

### Отправка картинки

1. Получить URL:
   ```bash
   curl -X POST "https://platform-api.max.ru/uploads?type=image" -H "Authorization: $TOKEN"
   ```
2. Залить файл по `url` — получить `{ "token": "..." }`.
3. Отправить сообщение:
   ```json
   {
     "text": "Фото",
     "attachments": [
       { "type": "image", "payload": { "token": "<token>" } }
     ]
   }
   ```

### Ответ на нажатие callback-кнопки

Прилетел `Update` c `update_type = "message_callback"` и полем `callback.callback_id = "abc"`:

```bash
curl -X POST "https://platform-api.max.ru/answers?callback_id=abc" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "notification": "Спасибо!" }'
```

### Настройка Webhook

```bash
curl -X POST "https://platform-api.max.ru/subscriptions" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://bot.example.com/hook",
    "update_types": ["message_created", "message_callback", "bot_started"],
    "secret": "supersecret_value_12345"
  }'
```

В обработчике вебхука всегда проверяйте заголовок `X-Max-Bot-Api-Secret` на совпадение с `supersecret_value_12345`.

---

# Полезные замечания

- **Максимум 30 rps** — закладывайте очередь/троттлинг в клиенте.
- **Редактирование и удаление сообщений** — только в течение **24 часов** с момента отправки.
- **Токен только в заголовке** (`Authorization`), query-параметр больше не поддерживается.
- Для **каналов** некоторые поля `Message` (`stat`, `url`) возвращаются, для диалогов и групп — нет.
- В методах пагинации (`GET /chats`, `GET /chats/{chatId}/members` и др.) для первой страницы передавайте `marker = null` (или не передавайте вовсе).
- В `POST /messages` **нельзя** передавать одновременно `user_id` и `chat_id` — только что-то одно.
- Для полноты информации по наследникам `User` (`UserWithPhoto`, `BotInfo`, `ChatMember`) и вспомогательным объектам (`Recipient`, `LinkedMessage`, `MessageBody`, `MessageStat`, `AttachmentRequest`, `NewMessageLink`, `Image`, `Subscription`, `BotCommand`, `ChatAdmin`, `FailedUserDetails`, `VideoUrls`, `PhotoAttachmentPayload`, `PhotoAttachmentRequestPayload`) см. официальную документацию — там доступны отдельные страницы для каждого типа.

---

*Документ составлен на основе [dev.max.ru/docs-api](https://dev.max.ru/docs-api).*
