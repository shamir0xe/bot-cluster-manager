from pydantic import BaseModel
from src.types.response_types import ResponseTypes


class StateData(BaseModel):
    bot_id: int = 0
    parent_id: int = -1
    state_id: int = 0
    data: str = ""
    keyboard_waiting: bool = False
    response_type: ResponseTypes = ResponseTypes.EDIT_TEXT
