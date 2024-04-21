from datetime import datetime
from typing import Optional
from telegram import User
from src.types.variable import Variable


class DatetimeVariable(Variable):
    pattern = "<:datetime>"

    @staticmethod
    def callback(**kwargs) -> str:
        return datetime.now().__str__()
