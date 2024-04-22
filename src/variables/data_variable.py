from src.models.state_data import StateData
from src.types.variable import Variable


class DataVariable(Variable):
    name = "data"

    @staticmethod
    def callback(state_data: StateData = StateData(), **kargs) -> str:
        return state_data.data

