from datetime import datetime
from typing import Optional
from telegram import User
from src.models.state_data import StateData
from src.types.variable import Variable


class StateNameVariable(Variable):
    pattern = "<:state_name>"

    @staticmethod
    def callback(state_data: StateData = StateData(), **kwargs) -> str:
        return state_data.name
