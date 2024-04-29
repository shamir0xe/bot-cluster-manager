from typing import Dict, Optional
from telegram import User
from src.models.utility.state_data import StateData
from src.types.variable import Variable


class ApplyVariables:
    @staticmethod
    def with_content(
        template: Optional[str],
        variables: Dict[str, Variable],
        state_data: StateData,
        user: Optional[User],
    ) -> str:
        if not template:
            return ""
        content = ""
        in_var_name = False
        i = 0
        sz = len(template)
        var = ""
        while i < sz:
            if in_var_name:
                if template[i] != ">":
                    var += template[i]
                else:
                    # end of the variable name
                    variable = var.split(".")[0]
                    args = var.split(".")[1:]
                    content += variables[variable].callback(
                        *args, state_data=state_data, user=user
                    )
                    var = ""
                    in_var_name = False
                i += 1
                continue
            else:
                if template[i : i + 2] == "<:":
                    in_var_name = True
                    i += 2
                    continue
                content += template[i]
                i += 1

        return content
