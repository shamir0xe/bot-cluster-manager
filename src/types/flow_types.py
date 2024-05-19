from enum import Enum


class FlowTypes(Enum):
    """It's the way users can interact with the bot"""

    AUDIO = "audio"
    VIDEO = "video"
    TEXT = "text"
    LOCATION = "location"
    PHOTO = "photo"
    CALLBACK = "callback"
    COMMAND = "command"
