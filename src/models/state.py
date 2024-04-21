from __future__ import annotations
from pydantic import BaseModel

from src.types.response_types import ResponseTypes


class State(BaseModel):
    bot_id: int = 0
    state_id: int = 0
    response_type: ResponseTypes = ResponseTypes.EDIT_TEXT

    @classmethod
    def build_with(cls, bot_id: int, state_id: int) -> State:
        # TODO
        state = cls()
        state.state_id = state_id
        state.bot_id = bot_id
        return state
