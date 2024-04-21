from typing import List, Optional
from telegram import User
from src.models.state_data import StateData
from src.types.variable import Variable


class ApplyVariables:
    @staticmethod
    def with_content(
        variables: List[Variable],
        template: str,
        bot_id: int,
        state_data: StateData,
        user: Optional[User],
    ) -> str:
        content = template
        for var in variables:
            content = content.replace(
                var.pattern,
                var.callback(data=state_data.data, user=user, bot_id=bot_id),
            )
        return content
