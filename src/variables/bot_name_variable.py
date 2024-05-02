from src.models.utility.state_data import StateData
from src.helpers.config.config import Config
from src.types.variable import Variable


class BotNameVariable(Variable):
    name = "bot_name"

    @staticmethod
    def callback(state_data: StateData = StateData.default(), **kwargs) -> str:
        return state_data.bot_name
