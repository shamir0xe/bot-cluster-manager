from datetime import datetime
from typing import Optional
from telegram import User
from src.helpers.config.config import Config
from src.types.variable import Variable


class BotNameVariable(Variable):
    pattern = "<:bot_name>"

    @staticmethod
    def callback(bot_id: int = 0, **kwargs) -> str:
        return Config(base_folder=f"src.bots.bot_{bot_id}.configs").read(
            "cfg.name", default="new-bot"
        )
