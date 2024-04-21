from typing import Optional
from telegram import User
from src.types.variable import Variable


class DataVariable(Variable):
    pattern = "<:data>"

    @staticmethod
    def callback(data: str = "", **kargs) -> str:
        return data

