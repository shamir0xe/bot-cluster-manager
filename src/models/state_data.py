from pydantic import BaseModel


class StateData(BaseModel):
    parent_id: int = -1
    state_id: int = 0
    data: str = ""
    keyboard_waiting: bool = False
