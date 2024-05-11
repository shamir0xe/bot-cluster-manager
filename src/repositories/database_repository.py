import functools
from typing import List
from src.helpers.config.config import Config
from src.models.bot.bot import Bot
from src.models.page.page import Page
from src.repositories.repository import Repository


class DatabaseRepository(Repository):
    def get_me(self, bot_id: int) -> Bot:
        data = {}
        bot_cfg = Config(base_folder=f"src.bots.bot_{bot_id}.configs").read("cfg")
        data["id"] = bot_cfg["id"]
        data["name"] = bot_cfg["name"]
        data["token"] = Config(base_folder=f"src.bots.bot_{bot_id}.configs").read(
            "env.token"
        )
        return Bot(**data)

    def get_pages(self, bot_id: int) -> List[Page]:
        pages = []
        data = Config(base_folder=f"src.bots.bot_{bot_id}.configs").read(
            "scenario.pages"
        )
        for page_data in data:
            pages += [Page(**page_data)]
        return pages

    def request_session(self, bot_id: int, telegram_id: str) -> str:
        return "good-old-fake-session-:)"

    def update_session(self, session_id: str, data: str) -> None:
        return
