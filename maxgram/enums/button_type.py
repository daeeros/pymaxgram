from enum import Enum


class ButtonType(str, Enum):
    CALLBACK = "callback"
    LINK = "link"
    REQUEST_CONTACT = "request_contact"
    REQUEST_GEO_LOCATION = "request_geo_location"
    OPEN_APP = "open_app"
    MESSAGE = "message"
    CLIPBOARD = "clipboard"
