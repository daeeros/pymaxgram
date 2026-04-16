# Классовые обработчики

## BaseHandler[T]

```python
class BaseHandler(BaseHandlerMixin[T], ABC, Generic[T]):
    def __init__(self, event: T, **kwargs: Any) -> None:
        self.event: T = event
        self.data: dict[str, Any] = kwargs

    @property
    def bot(self) -> Bot: ...      # data["bot"]

    @property
    def update(self) -> Update: ... # data["event_update"]

    @abstractmethod
    async def handle(self) -> Any: ...

    def __await__(self): ...        # Позволяет await handler
```

## MessageHandler

```python
class MessageHandler(BaseHandler[Message], ABC):
    @property
    def from_user(self) -> User | None  # message.sender

    @property
    def chat_id(self) -> int | None  # message.recipient.chat_id
```

## CallbackHandler

```python
class CallbackHandler(BaseHandler[Callback], ABC):
    @property
    def from_user(self) -> User  # callback.user

    @property
    def message(self) -> Message | None  # callback.message
```

## BotStartedHandler

```python
class BotStartedHandler(BaseHandler[Update], ABC):
    @property
    def from_user(self) -> User | None  # update.user

    @property
    def chat_id(self) -> int | None  # update.chat_id
```

## ErrorHandler

```python
class ErrorHandler(BaseHandler[Exception], ABC):
    @property
    def exception_name(self) -> str  # type(exception).__name__

    @property
    def exception_message(self) -> str  # str(exception)
```

## MessageHandlerCommandMixin

```python
class MessageHandlerCommandMixin(BaseHandlerMixin[Message]):
    @property
    def command(self) -> CommandObject | None  # data.get("command")
```

## Исходные файлы

- `maxgram/handlers/base.py`
- `maxgram/handlers/message.py`
- `maxgram/handlers/callback.py`
- `maxgram/handlers/bot_started.py`
- `maxgram/handlers/error.py`
