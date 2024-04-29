from src.models.utility.state_data import StateData
from src.types.variable import Variable


class DataVariable(Variable):
    name = "data"

    @staticmethod
    def callback(*args, state_data: StateData = StateData(), **kargs) -> str:
        for arg in args:
            value = state_data.variables.get(arg)
            if value is not None:
                return value
        return ""
