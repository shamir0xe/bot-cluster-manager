import functools
from typing import List

from src.models.bot import Bot
from src.models.page import Page
from src.repositories.repository import Repository
# from src.facades.network import Network


class ApiRepository(Repository):
    def get_me(self, bot_id: int) -> Bot:
        # query = ""
        # response = Network.query(query)
        # return Bot(**response)
        return Bot(**{})

    @functools.lru_cache
    def get_pages(self, bot_id: int) -> List[Page]:
        return super().get_pages(bot_id)
