from enum import Enum


class ChatAdminPermission(str, Enum):
    READ_ALL_MESSAGES = "read_all_messages"
    ADD_REMOVE_MEMBERS = "add_remove_members"
    ADD_ADMINS = "add_admins"
    CHANGE_CHAT_INFO = "change_chat_info"
    PIN_MESSAGE = "pin_message"
    WRITE = "write"
    CAN_CALL = "can_call"
    EDIT_LINK = "edit_link"
    POST_EDIT_DELETE_MESSAGE = "post_edit_delete_message"
    EDIT_MESSAGE = "edit_message"
    DELETE_MESSAGE = "delete_message"
