from src.models.state_data import StateData
from src.types.variable import Variable


class ParentVariable(Variable):
    name = "parent"

    @staticmethod
    def callback(*args, state_data: StateData = StateData(), **kargs) -> str:
        for arg in args:
            if arg == "name":
                return state_data.parent.name
            if arg == "response_type":
                return state_data.parent.response_type.value
        return ""
