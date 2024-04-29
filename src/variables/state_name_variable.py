from src.models.utility.state_data import StateData
from src.types.variable import Variable


class StateNameVariable(Variable):
    name = "state_name"

    @staticmethod
    def callback(state_data: StateData = StateData(), **kwargs) -> str:
        return state_data.name
