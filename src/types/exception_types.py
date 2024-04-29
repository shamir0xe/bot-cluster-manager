from enum import Enum


class ExceptionTypes(Enum):
    NETWORK_ERROR = "network-error"
    PAGE_NOT_FOUND = "page-not-found"
    NOT_STARTED = "not-started"
