import functools
import json
from typing import List
from pylib_0xe.json.json_helper import JsonHelper
from src.helpers.builders.query_builder import QueryBuilder
from src.models.bot.bot import Bot
from src.models.page.page import Page
from src.repositories.repository import Repository
from src.facades.network import Network
from src.types.exception_types import ExceptionTypes


class ApiRepository(Repository):
    def get_me(self, bot_id: int) -> Bot:
        response = Network.query(QueryBuilder.bot_info(bot_id=bot_id).build())
        if response:
            return Bot(**response)
        raise Exception(ExceptionTypes.NETWORK_ERROR)

    def get_pages(self, bot_id: int) -> List[Page]:
        response = Network.query(QueryBuilder.get_pages(bot_id=bot_id).build())
        pages = []
        if response and "pages" in response:
            pages_json = JsonHelper.selector_get_value(
                json.loads(response["pages"]), "pages"
            )
            for page_data in pages_json:
                pages += [Page(**page_data)]
        return pages

    def request_session(self, bot_id: int, telegram_id: str) -> str:
        response = Network.query(
            QueryBuilder.request_session(bot_id=bot_id, telegram_id=telegram_id).build()
        )
        if response:
            return response["id"]
        raise Exception(ExceptionTypes.NETWORK_ERROR)

    def update_session(self, session_id: str, data: str) -> None:
        response = Network.query(
            QueryBuilder.update_session(session_id=session_id, data=data).build()
        )
        if not response:
            raise Exception(ExceptionTypes.NETWORK_ERROR)
