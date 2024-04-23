from typing import Dict
from pydantic import BaseModel, Field
from src.models.parent_page import ParentPage
from src.types.response_types import ResponseTypes


class StateData(BaseModel):
    bot_id: int = 0
    parent: ParentPage = Field(default_factory=ParentPage)
    name: str = "start"
    ## variables that each user defines in process of the survey
    variables: Dict[str, str] = Field(default_factory=dict)
    keyboard_waiting: bool = False
    response_type: ResponseTypes = ResponseTypes.EDIT_TEXT
    decisions: Dict[str, str] = Field(default_factory=dict)

    @staticmethod
    def default():
        return StateData()
