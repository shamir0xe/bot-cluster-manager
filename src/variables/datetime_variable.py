from datetime import datetime
from typing import Optional
from telegram import User
from src.types.variable import Variable


class DatetimeVariable(Variable):
    name = "datetime"

    @staticmethod
    def callback(*args, **kwargs) -> str:
        if "hour" in args:
            return str(datetime.now().hour)
        if "minute" in args:
            return str(datetime.now().minute)
        if "seconds" in args:
            return str(datetime.now().second)
        if "year" in args:
            return str(datetime.now().year)
        if "day" in args:
            return str(datetime.now().day)
        if "month" in args:
            return str(datetime.now().month)
        return datetime.now().__str__()
