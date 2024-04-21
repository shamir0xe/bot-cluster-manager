from pydantic import BaseModel
from src.types.response_types import ResponseTypes


class StateData(BaseModel):
    bot_id: int = 0
    parent_id: int = -1
    name: str = "start"
    data: str = ""
    keyboard_waiting: bool = False
    response_type: ResponseTypes = ResponseTypes.EDIT_TEXT

    @staticmethod
    def default():
        return StateData()
