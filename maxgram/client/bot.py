from __future__ import annotations

from types import TracebackType
from typing import (
    Any,
    TypeVar,
)

from ..methods import (
    AddMembers,
    AnswerCallback,
    AssignAdmins,
    CreateSubscription,
    DeleteChat,
    DeleteSubscription,
    EditBotInfo,
    EditChat,
    EditMessage,
    GetAdmins,
    GetChat,
    GetChatByLink,
    GetChats,
    GetMe,
    GetMembers,
    GetMessageById,
    GetMessages,
    GetMyMembership,
    GetPinnedMessage,
    GetSubscriptions,
    GetUpdates,
    GetUploadUrl,
    GetVideoInfo,
    LeaveChat,
    MaxMethod,
    PinMessage,
    RemoveAdmin,
    RemoveMember,
    SendAction,
    SendMessage,
    UnpinMessage,
)
from ..methods.base import MaxType
from ..types import (
    BotCommand,
    BotInfo,
    Chat,
    ChatMember,
    Message,
    Subscription,
    Update,
    UploadInfo,
    User,
    VideoInfo,
)
from .context_controller import BotContextController
from .default import DefaultBotProperties

T = TypeVar("T")


class Bot:
    """MAX Bot API client."""

    def __init__(
        self,
        token: str,
        session: Any | None = None,
        default: DefaultBotProperties | None = None,
        **kwargs: Any,
    ) -> None:
        if not token:
            raise ValueError("Token must not be empty")

        self.__token = token
        self.session = session or self._create_default_session()
        self.default = default or DefaultBotProperties()
        self._me: BotInfo | None = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def _create_default_session() -> Any:
        from .session.aiohttp import AiohttpSession
        return AiohttpSession()

    @property
    def token(self) -> str:
        return self.__token

    @property
    def id(self) -> int | None:
        """Bot ID. Available after calling get_me()."""
        if self._me:
            return self._me.user_id
        return None

    @property
    def username(self) -> str | None:
        """Bot username. Available after calling get_me()."""
        if self._me:
            return self._me.username
        return None

    async def me(self) -> BotInfo:
        """Get bot info (cached)."""
        if self._me is None:
            self._me = await self.get_me()
        return self._me

    async def __call__(
        self,
        method: MaxMethod[MaxType],
        **kwargs: Any,
    ) -> MaxType:
        """Execute an API method."""
        if getattr(self, '_requests_debug', False):
            import logging
            _log = logging.getLogger("maxgram.request")
            path = method.build_request_path()
            body = method.build_request_body() if method.__http_method__ in ("POST", "PUT", "PATCH") else None
            params = method.build_query_params()
            _log.info(
                "%s %s params=%s body=%s",
                method.__http_method__, path,
                params or None,
                body,
            )
        result = await self.session(self, method, **kwargs)
        if getattr(self, '_requests_debug', False):
            _log.info("  -> %s", type(result).__name__)
        return result

    def __hash__(self) -> int:
        return hash(self.__token)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bot):
            return NotImplemented
        return self.__token == other.__token

    async def __aenter__(self) -> Bot:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.session.close()

    # ==================== Bot Info ====================

    async def get_me(self) -> BotInfo:
        return await self(GetMe())

    async def edit_info(
        self,
        name: str | None = None,
        description: str | None = None,
        commands: list[BotCommand] | None = None,
        photo: dict[str, Any] | None = None,
    ) -> BotInfo:
        return await self(
            EditBotInfo(
                name=name,
                description=description,
                commands=commands,
                photo=photo,
            )
        )

    async def set_commands(self, commands: list[BotCommand]) -> BotInfo:
        return await self.edit_info(commands=commands)

    async def delete_commands(self) -> BotInfo:
        return await self.edit_info(commands=[])

    # ==================== Chats ====================

    async def get_chats(
        self,
        count: int | None = None,
        marker: int | None = None,
    ) -> list[Chat]:
        return await self(GetChats(count=count, marker=marker))

    async def get_chat(self, chat_id: int) -> Chat:
        return await self(GetChat(chat_id=chat_id))

    async def get_chat_by_link(self, chat_link: str) -> Chat:
        return await self(GetChatByLink(chat_link=chat_link))

    async def edit_chat(
        self,
        chat_id: int,
        title: str | None = None,
        icon: dict[str, Any] | None = None,
        pin: str | None = None,
        notify: bool | None = None,
    ) -> Chat:
        return await self(EditChat(
            chat_id=chat_id, title=title, icon=icon, pin=pin, notify=notify,
        ))

    async def delete_chat(self, chat_id: int) -> bool:
        return await self(DeleteChat(chat_id=chat_id))

    # ==================== Chat Actions ====================

    async def send_action(self, chat_id: int, action: str) -> bool:
        return await self(SendAction(chat_id=chat_id, action=action))

    # ==================== Pinned Messages ====================

    async def get_pinned_message(self, chat_id: int) -> Message | None:
        return await self(GetPinnedMessage(chat_id=chat_id))

    async def pin_message(
        self,
        chat_id: int,
        message_id: str,
        notify: bool | None = None,
    ) -> bool:
        return await self(PinMessage(chat_id=chat_id, message_id=message_id, notify=notify))

    async def unpin_message(self, chat_id: int) -> bool:
        return await self(UnpinMessage(chat_id=chat_id))

    # ==================== Members ====================

    async def get_my_membership(self, chat_id: int) -> ChatMember:
        return await self(GetMyMembership(chat_id=chat_id))

    async def leave_chat(self, chat_id: int) -> bool:
        return await self(LeaveChat(chat_id=chat_id))

    async def get_admins(
        self,
        chat_id: int,
        marker: int | None = None,
    ) -> list[ChatMember]:
        return await self(GetAdmins(chat_id=chat_id, marker=marker))

    async def assign_admins(
        self,
        chat_id: int,
        admins: list[dict[str, Any]],
    ) -> bool:
        return await self(AssignAdmins(chat_id=chat_id, admins=admins))

    async def remove_admin(self, chat_id: int, user_id: int) -> bool:
        return await self(RemoveAdmin(chat_id=chat_id, user_id=user_id))

    async def get_members(
        self,
        chat_id: int,
        user_ids: list[int] | None = None,
        marker: int | None = None,
        count: int | None = None,
    ) -> list[ChatMember]:
        return await self(GetMembers(
            chat_id=chat_id, user_ids=user_ids, marker=marker, count=count,
        ))

    async def add_members(self, chat_id: int, user_ids: list[int]) -> bool:
        return await self(AddMembers(chat_id=chat_id, user_ids=user_ids))

    async def remove_member(
        self,
        chat_id: int,
        user_id: int,
        block: bool | None = None,
    ) -> bool:
        return await self(RemoveMember(chat_id=chat_id, user_id=user_id, block=block))

    # ==================== Subscriptions (Webhooks) ====================

    async def get_subscriptions(self) -> list[Subscription]:
        return await self(GetSubscriptions())

    async def create_subscription(
        self,
        url: str,
        update_types: list[str] | None = None,
        secret: str | None = None,
    ) -> bool:
        return await self(CreateSubscription(
            url=url, update_types=update_types, secret=secret,
        ))

    async def delete_subscription(self, url: str) -> bool:
        return await self(DeleteSubscription(url=url))

    # ==================== Updates ====================

    async def get_updates(
        self,
        limit: int | None = None,
        timeout: int | None = None,
        marker: int | None = None,
        types: list[str] | None = None,
    ) -> list[Update]:
        return await self(GetUpdates(
            limit=limit, timeout=timeout, marker=marker, types=types,
        ))

    # ==================== Messages ====================

    async def send_message(
        self,
        chat_id: int | None = None,
        user_id: int | None = None,
        text: str | None = None,
        attachments: list[Any] | None = None,
        link: Any | None = None,
        notify: bool | None = None,
        format: str | None = None,
        disable_link_preview: bool | None = None,
        keyboard: Any | None = None,
    ) -> Message:
        from ..utils.keyboard import prepare_keyboard

        if format is None and self.default.parse_mode:
            format = self.default.parse_mode
        if notify is None and self.default.notify is not None:
            notify = self.default.notify
        if disable_link_preview is None and self.default.disable_link_preview is not None:
            disable_link_preview = self.default.disable_link_preview
        attachments = prepare_keyboard(attachments, keyboard)
        return await self(SendMessage(
            chat_id=chat_id,
            user_id=user_id,
            text=text,
            attachments=attachments,
            link=link,
            notify=notify,
            format=format,
            disable_link_preview=disable_link_preview,
        ))

    async def edit_message(
        self,
        message_id: str,
        text: str | None = None,
        attachments: list[Any] | None = None,
        notify: bool | None = None,
        format: str | None = None,
        keyboard: Any | None = None,
    ) -> bool:
        from ..utils.keyboard import prepare_keyboard

        if format is None and self.default.parse_mode:
            format = self.default.parse_mode
        attachments = prepare_keyboard(attachments, keyboard)
        if attachments is None:
            attachments = []
        return await self(EditMessage(
            message_id=message_id,
            text=text,
            attachments=attachments,
            notify=notify,
            format=format,
        ))

    async def get_messages(
        self,
        chat_id: int | None = None,
        message_ids: list[str] | None = None,
        from_: int | None = None,
        to: int | None = None,
        count: int | None = None,
    ) -> list[Message]:
        return await self(GetMessages(
            chat_id=chat_id, message_ids=message_ids,
            from_=from_, to=to, count=count,
        ))

    async def get_message_by_id(self, message_id: str) -> Message:
        return await self(GetMessageById(message_id=message_id))

    # ==================== Uploads ====================

    async def get_upload_url(self, type: str) -> UploadInfo:
        return await self(GetUploadUrl(type=type))

    async def upload_file(
        self,
        file_type: str,
        file_data: bytes,
        filename: str = "file",
    ) -> str:
        """Two-stage file upload. Returns token for use in attachments."""
        upload_info = await self.get_upload_url(type=file_type)
        result = await self.session.upload_file(
            bot=self,
            upload_url=upload_info.url,
            file_data=file_data,
            filename=filename,
        )
        return result.get("token", upload_info.token or "")

    # ==================== Video ====================

    async def get_video_info(self, video_token: str) -> VideoInfo:
        return await self(GetVideoInfo(video_token=video_token))

    # ==================== Callbacks ====================

    async def answer_callback(
        self,
        callback_id: str,
        text: str | None = None,
        attachments: list[Any] | None = None,
        notification: str | None = None,
        notify: bool | None = None,
        format: str | None = None,
        keyboard: Any | None = None,
    ) -> bool:
        from ..utils.keyboard import prepare_keyboard

        if text is not None and format is None and self.default.parse_mode:
            format = self.default.parse_mode
        attachments = prepare_keyboard(attachments, keyboard)
        return await self(AnswerCallback(
            callback_id=callback_id,
            text=text,
            attachments=attachments,
            notification=notification,
            notify=notify,
            format=format,
        ))
