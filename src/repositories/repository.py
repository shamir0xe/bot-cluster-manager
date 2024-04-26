from abc import ABC, abstractmethod
import functools
from typing import List

from src.models.bot import Bot
from src.models.page import Page


class Repository(ABC):
    @abstractmethod
    def get_me(self, bot_id: int) -> Bot:
        pass

    @abstractmethod
    @functools.cache
    def get_pages(self, bot_id: int) -> List[Page]:
        pass
