# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**pymaxgram** — async Python framework for MAX Messenger Bot API. Built on asyncio + aiohttp + pydantic v2. Python 3.10+.

## Build & Development

```bash
pip install hatch
hatch build          # build wheel + sdist
hatch publish        # publish to PyPI (needs PYPI_API_TOKEN)
```

Version is in `maxgram/__meta__.py`. CI auto-bumps patch on push to main.

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
- **`Router`** (`dispatcher/router.py`) — 15 event observers (`message`, `message_callback`, `bot_started`, `bot_stopped`, `bot_added`, `bot_removed`, `user_added`, `user_removed`, `message_edited`, `message_removed`, `chat_title_changed`, `dialog_muted`, `dialog_unmuted`, `dialog_cleared`, `dialog_removed`) + `error`, `startup`, `shutdown`.
- **`MaxObject`** (`types/base.py`) — Base Pydantic model: `frozen=True`, `extra="allow"`, `defer_build=True`. UNSET sentinel for optional params.
- **`Update`** (`types/update.py`) — Incoming event. `model_validator(mode="before")` copies `message` into `callback` for `message_callback` type. `event` property returns typed subclass via `EVENT_TYPE_MAP`.

### Typed Events (`types/events.py`)

Each `update_type` returns a typed class: `BotStarted`, `BotStopped`, `BotAdded`, `BotRemoved`, `UserAdded`, `UserRemoved`, `ChatTitleChanged`, `MessageRemoved`, `DialogMuted`, `DialogUnmuted`, `DialogCleared`, `DialogRemoved`. Message-based types return `Message` or `Callback` directly.

### Method Pattern (`methods/base.py`)

All API methods inherit `MaxMethod[ReturnType]` with class vars `__returning__`, `__http_method__`, `__api_path__`, `__item_type__` (for list methods). Methods: `build_request_path()`, `build_query_params()`, `build_request_body()`.

### Response Parsing (`client/session/base.py`)

`check_response()` handles: bool methods (success/message pattern), list methods (extracts from known keys + validates via `__item_type__`), single objects (model_validate). Also auto-updates `method.marker` for pagination.

### Middleware

`BaseMiddleware.__call__(handler, event, data) -> Any`. Outer middleware runs for all events; inner only when handler matched. Built-in: `ErrorsMiddleware`, `UserContextMiddleware`, `FSMContextMiddleware`.

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
