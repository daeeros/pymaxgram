from enum import Enum


class ChatAdminPermission(str, Enum):
    READ_ALL_MESSAGES = "read_all_messages"
    ADD_REMOVE_MEMBERS = "add_remove_members"
    ADD_ADMINS = "add_admins"
    CHANGE_CHAT_INFO = "change_chat_info"
    PIN_MESSAGE = "pin_message"
    WRITE = "write"
    EDIT = "edit"
    DELETE = "delete"
    CAN_CALL = "can_call"
    EDIT_LINK = "edit_link"
    VIEW_STATS = "view_stats"
    # Legacy names - MAX may still return them next to edit/delete/write
    POST_EDIT_DELETE_MESSAGE = "post_edit_delete_message"
    EDIT_MESSAGE = "edit_message"
    DELETE_MESSAGE = "delete_message"
