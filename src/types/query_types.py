from enum import Enum


class QueryTypes(Enum):
    LOGIN = "login"
    BOT_INFO = "bot-info"
    REQUEST_SESSION = "request-session"
    UPDATE_SESSION = "update-session"
    GET_PAGES = "get-pages"
