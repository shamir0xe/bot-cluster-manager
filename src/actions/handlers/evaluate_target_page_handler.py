from typing import Dict, List, Optional

from telegram import User
from src.models.page.conditional_proposition import ConditionalProposition
from src.actions.conditional_proposition_evaluator import (
    ConditionalPropositionEvaluator,
)
from src.models.utility.state_data import StateData
from src.types.variable import Variable


class EvaluateTargetPageHandler:
    """evaluate which page should be heading to"""

    @staticmethod
    def with_flow(
        flow: List[ConditionalProposition],
        user: Optional[User],
        state_data: StateData,
        variables: Dict[str, Variable],
        default: str = "",
    ) -> str:
        going_to = default
        if flow:
            going_to = ConditionalPropositionEvaluator.eval(
                propositions=flow,
                variables=variables,
                state_data=state_data,
                user=user,
            )
        ## updaing parent's name
        EvaluateTargetPageHandler.update_parent_info(state_data, going_to)
        return going_to

    @staticmethod
    def update_parent_info(state_data: StateData, target_page: str):
        if state_data.name != target_page:
            state_data.parent.name = state_data.name
        state_data.name = target_page
