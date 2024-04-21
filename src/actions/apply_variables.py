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
            length = len(var.pattern)
            idx = content.find(var.pattern)
            if idx > 0:
                new_str = var.callback(data=state_data.data, user=user, bot_id=bot_id)
                bidx = 0
                while idx > bidx + len(new_str):
                    content = content[:idx] + new_str + content[idx + length :]
                    bidx = idx
                    idx = content.find(var.pattern)
        print(f"after edit: content = {content}")
        return content
