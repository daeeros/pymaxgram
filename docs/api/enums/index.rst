=============
Перечисления
=============

.. module:: maxgram.enums

AttachmentType
--------------

.. code-block:: python

   class AttachmentType(str, Enum):
       IMAGE = "image"
       VIDEO = "video"
       AUDIO = "audio"
       FILE = "file"
       STICKER = "sticker"
       CONTACT = "contact"
       INLINE_KEYBOARD = "inline_keyboard"
       LOCATION = "location"
       SHARE = "share"

ButtonType
----------

.. code-block:: python

   class ButtonType(str, Enum):
       CALLBACK = "callback"
       LINK = "link"
       REQUEST_CONTACT = "request_contact"
       REQUEST_GEO_LOCATION = "request_geo_location"
       OPEN_APP = "open_app"
       MESSAGE = "message"
       CLIPBOARD = "clipboard"

ChatAction
----------

.. code-block:: python

   class ChatAction(str, Enum):
       TYPING_ON = "typing_on"
       SENDING_PHOTO = "sending_photo"
       SENDING_VIDEO = "sending_video"
       SENDING_AUDIO = "sending_audio"
       SENDING_FILE = "sending_file"
       MARK_SEEN = "mark_seen"

ChatAdminPermission
-------------------

.. code-block:: python

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

ChatStatus
----------

.. code-block:: python

   class ChatStatus(str, Enum):
       ACTIVE = "active"
       REMOVED = "removed"
       LEFT = "left"
       CLOSED = "closed"

ContentType
-----------

.. code-block:: python

   class ContentType(str, Enum):
       TEXT = "text"
       IMAGE = "image"
       VIDEO = "video"
       AUDIO = "audio"
       FILE = "file"
       STICKER = "sticker"
       CONTACT = "contact"
       LOCATION = "location"
       SHARE = "share"
       INLINE_KEYBOARD = "inline_keyboard"

MarkupType
----------

.. code-block:: python

   class MarkupType(str, Enum):
       STRONG = "strong"
       EMPHASIZED = "emphasized"
       MONOSPACED = "monospaced"
       LINK = "link"
       STRIKETHROUGH = "strikethrough"
       UNDERLINE = "underline"
       USER_MENTION = "user_mention"

ParseMode
---------

.. code-block:: python

   class ParseMode(str, Enum):
       MARKDOWN = "markdown"
       HTML = "html"

UpdateType
----------

.. code-block:: python

   class UpdateType(str, Enum):
       MESSAGE_CREATED = "message_created"
       MESSAGE_CALLBACK = "message_callback"
       MESSAGE_EDITED = "message_edited"
       MESSAGE_REMOVED = "message_removed"
       BOT_STARTED = "bot_started"
       BOT_STOPPED = "bot_stopped"
       BOT_ADDED = "bot_added"
       BOT_REMOVED = "bot_removed"
       USER_ADDED = "user_added"
       USER_REMOVED = "user_removed"
       CHAT_TITLE_CHANGED = "chat_title_changed"
       DIALOG_MUTED = "dialog_muted"
       DIALOG_UNMUTED = "dialog_unmuted"
       DIALOG_CLEARED = "dialog_cleared"
       DIALOG_REMOVED = "dialog_removed"

UploadType
----------

.. code-block:: python

   class UploadType(str, Enum):
       IMAGE = "image"
       VIDEO = "video"
       AUDIO = "audio"
       FILE = "file"

Исходные файлы
--------------

``maxgram/enums/*.py``
