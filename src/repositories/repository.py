from abc import ABC, abstractmethod
import functools
from typing import List

from src.models.bot.bot import Bot
from src.models.page.page import Page


class Repository(ABC):
    @abstractmethod
    def get_me(self, bot_id: int) -> Bot:
        """Retrieve informations of the bot with bot_id"""
        pass

    @abstractmethod
    @functools.cache
    def get_pages(self, bot_id: int) -> List[Page]:
        """Get the pages of bot with bot_id"""
        pass

    @abstractmethod
    def request_session(self, bot_id: int, telegram_id: str) -> str:
        """Request new session from the server"""
        pass

    @abstractmethod
    def update_session(self, session_id: str, data: str) -> None:
        """Update session data"""
        pass
