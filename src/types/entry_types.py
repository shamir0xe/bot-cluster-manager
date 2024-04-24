from enum import Enum


class EntryTypes(Enum):
    COMMAND = "command"
    MESSAGE = "message"
    CALLBACK = "callback"
    PHOTO = "photo"
    VIDEO = "video"
    FILE = "file"
