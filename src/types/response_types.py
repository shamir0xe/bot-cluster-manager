from enum import Enum


class ResponseTypes(Enum):
    EDIT_TEXT = "edit_text"
    MESSAGE = "message"
    PHOTO = "photo"
    VIDEO = "video"
    LOCATION = "location"
