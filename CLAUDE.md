# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**pymaxgram** — async Python framework for MAX Messenger Bot API. Built on asyncio + aiohttp + pydantic v2. Python 3.10+.

## Build & Development

```bash
pip install hatch
hatch build          # build wheel + sdist
```

Version is in `maxgram/__meta__.py`. CI auto-bumps patch on push to main and pushes a `vX.Y.Z` tag. Not published to PyPI anymore — consumers install from git pinned to a tag: `pymaxgram[fastapi] @ git+https://github.com/daeeros/pymaxgram.git@vX.Y.Z`.

### Documentation (Sphinx)

```bash
cd docs
pip install -r requirements.txt
make html            # output: docs/_build/html/
```

### No test suite currently exists.

## Architecture

### Core Flow

```
MAX API → Bot.get_updates() → Update → Dispatcher → Router tree → Observer → Filters → Handler
```

### Key Classes

- **`Bot`** (`client/bot.py`) — HTTP client wrapping all MAX API methods. Accepts `**kwargs` as custom attributes. `DefaultBotProperties` for parse_mode/notify defaults that auto-apply to all send methods.
- **`Dispatcher`** (`dispatcher/dispatcher.py`) — Root Router. Manages polling loop, FSM middleware, error handling. `updates_debug`/`requests_debug` flags for logging.
- **`Router`** (`dispatcher/router.py`) — 19 event observers (`message`, `message_callback`, `bot_started`, `bot_stopped`, `bot_added`, `bot_removed`, `user_added`, `user_removed`, `message_edited`, `message_removed`, `comment` (`comment_created`), `comment_edited`, `comment_removed`, `chat_title_changed`, `dialog_muted`, `dialog_unmuted`, `dialog_cleared`, `dialog_removed`, `bot_admin_permissions_changed`) + `error`, `startup`, `shutdown`.
- **`MaxObject`** (`types/base.py`) — Base Pydantic model: `frozen=True`, `extra="allow"`, `defer_build=True`. UNSET sentinel for optional params.
- **`Update`** (`types/update.py`) — Incoming event. `model_validator(mode="before")` copies `message` into `callback` for `message_callback` type. `event` property returns typed subclass via `EVENT_TYPE_MAP`.

### Typed Events (`types/events.py`)

Each `update_type` returns a typed class: `BotStarted`, `BotStopped`, `BotAdded`, `BotRemoved`, `UserAdded`, `UserRemoved`, `ChatTitleChanged`, `MessageRemoved`, `CommentRemoved`, `BotAdminPermissionsChanged`, `DialogMuted`, `DialogUnmuted`, `DialogCleared`, `DialogRemoved`. Message-based types (`message_created`, `message_edited`, `comment_created`, `comment_edited`) return `Message`, `message_callback` returns `Callback`.

MAX sends some `message_created` updates with no `message` at all (raw body is just `{"timestamp":...,"update_type":"message_created"}`, tens of thousands a day for a bot in many groups). `Update.event` raises `EmptyUpdateError` (subclass of `UpdateTypeLookupError`) for a known message-type update without its payload; `Dispatcher._listen_update` skips it with a DEBUG log instead of the per-update `RuntimeWarning` reserved for truly unknown types.

### Method Pattern (`methods/base.py`)

All API methods inherit `MaxMethod[ReturnType]` with class vars `__returning__`, `__http_method__`, `__api_path__`, `__item_type__` (for list methods). Methods: `build_request_path()`, `build_query_params()`, `build_request_body()`.

### Response Parsing (`client/session/base.py`)

`check_response()` handles: bool methods (success/message pattern), list methods (extracts from known keys + validates via `__item_type__`), single objects (model_validate). Also auto-updates `method.marker` for pagination.

### Middleware

`BaseMiddleware.__call__(handler, event, data) -> Any`. Outer middleware runs for all events; inner only when handler matched. Built-in: `ErrorsMiddleware`, `UserContextMiddleware`, `FSMContextMiddleware`.

### Comments

Comments under channel posts: `GetComments`, `GetComment`, `SendComment`, `EditComment`, `DeleteComment` (`/messages/{message_id}/comments`, `message_id` is the post `mid`). They return/carry `CommentMessage` (no `url`, body without attachments). Edit/delete pass `comment_id` as a query param; `POST` returns `{"message": CommentMessage}` which `check_response` unwraps. Comment updates: `comment_created`/`comment_edited` carry a `Message`, `comment_removed` → `CommentRemoved` with `post_id`. The bot never gets updates for its own comments.

### Webhook background tasks

`WebhookProcessor` (`webhook/core.py`) runs each update in `_feed_in_background`, which swallows handler exceptions (the dispatcher already logged them) and logs parse failures. Never let these tasks end with an exception: asyncio then logs "Task exception was never retrieved" from `Task.__del__` during GC, in whatever thread runs the collector — inside a loguru `enqueue=True` worker that deadlocks the whole process.

On stop, in-flight update tasks are drained (`utils/tasks.py:drain_tasks`, 15 s, then cancelled) before shutdown hooks and the bot session close: `WebhookProcessor.drain()` in every webhook backend, `_handle_update_tasks` in `start_polling`. Apps close their DB right after the webhook/polling stops, so without the drain handlers still running hit a closed pool. The FastAPI backend also turns an external cancel of its task into a proper `uvicorn` shutdown (socket close + lifespan shutdown). The aiohttp handler keeps one `WebhookProcessor` per bot — its task set holds the only strong refs to the background tasks.

### Channels

Channel posts arrive as ordinary `message_created` updates — there is no channel-specific `update_type`. The bot must be a channel admin (`read_all_messages` + `write` is enough). Identify a channel post via `Message.is_channel_post` / `recipient.chat_type == "channel"`; `stat` and `url` are NOT populated on incoming updates despite the API reference. Channel posts have no `sender`. The bot's own messages do not come back as `message_created`. Filters: `ChannelPost()` / `ChatTypeFilter(*types)` in `filters/chat_type.py`.

### Keyboard Helper

`keyboard=` parameter on `message.answer()`, `message.reply()`, `callback.answer()`, `bot.send_message()` etc. accepts `InlineKeyboardBuilder`, `InlineKeyboard`, or `list[list[Button]]`. Converted via `prepare_keyboard()` in `utils/keyboard.py`.

### Formatting

`utils/formatting.py` — HTML-only elements: `Bold`, `Italic`, `Underline`, `Strikethrough`, `Code`, `Pre`, `TextLink`, `UserMention`. `as_list()`, `as_marked_list()`, `as_key_value()` etc.

`utils/text_decorations.py` — `html` and `md` decoration instances for raw string formatting.

### Markup Parsing

`MessageBody.markup` — `list[MarkupElement]` with types: `strong`, `emphasized`, `monospaced`, `link`, `strikethrough`, `underline`, `user_mention`. Field `from` aliased as `from_pos` in Python.

## Important Patterns

- MAX API puts `message` at Update level for `message_callback`, not inside `callback`. Handled by `model_validator` on `Update`.
- `callback.answer(text=..., keyboard=...)` edits message via `POST /answers`. Preferred over `callback.edit_text()` + separate `callback.answer()`.
- Exceptions renamed: `MaxgramError` (not AiogramError), `DetailedMaxgramError`, `MaxgramWarning`.
- `User.full_name`, `User.mention_html`, `User.mention_md` — computed properties.
- `BotStarted.deep_link(decoder=...)` — decodes base64url payload.
- `Bot.username` property available after `get_me()`.

## MAX Bot API Reference

Full API spec in `max-bot-api.md`. Key differences from Telegram:
- Auth: `Authorization: <token>` header only (no query params)
- Formatting: `<b>`, `<i>`, `<s>`, `<u>`, `<code>`, `<pre>`, `<a href>` for HTML; `**`, `*`, `~~`, `++`, `` ` ``, `[]()` for Markdown. No spoiler/blockquote support.
- Callback answer: `POST /answers` with `message` (edit) and/or `notification` (toast)
- Max 30 rps, 4GB file uploads, 4000 char message limit, 128 byte callback payload
- `PATCH /me` is gone (404 `method.not.found`) — bot commands are set via `PATCH /me/commands` (`EditBotCommands`, returns `{"commands": [...]}`); name/description/photo can't be changed via the API anymore
- `link.type="forward"` requires an empty `text` (otherwise `errors.forward.text.not-empty`)
- `Chat.type` really is `dialog`/`chat`/`channel` and responses carry an undocumented `messages_count`, despite what `max-bot-api.md` claims — the spec file carries inline corrections
