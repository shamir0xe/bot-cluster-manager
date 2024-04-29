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

    @functools.lru_cache
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
