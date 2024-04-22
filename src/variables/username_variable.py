from typing import Optional
from telegram import User
from src.types.variable import Variable


class UsernameVariable(Variable):
    name = "username"

    @staticmethod
    def callback(user: Optional[User] = None, **kwargs) -> str:
        if user and user.username:
            return user.username
        return ""
