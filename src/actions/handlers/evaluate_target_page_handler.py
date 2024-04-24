from typing import Dict, Optional

from telegram import User
from src.actions.conditional_proposition_evaluator import (
    ConditionalPropositionEvaluator,
)
from src.models.page import Page
from src.models.state_data import StateData
from src.types.variable import Variable


class EvaluateTargetPageHandler:
    """evaluate which page should be heading to"""

    @staticmethod
    def from_photo(
        state_data: StateData,
        user: Optional[User],
        parent_page: Page,
        variables: Dict[str, Variable],
    ) -> str:
        going_to = parent_page.name
        if parent_page.flow and parent_page.flow.photo:
            going_to = ConditionalPropositionEvaluator.eval(
                propositions=parent_page.flow.photo.fn,
                variables=variables,
                state_data=state_data,
                user=user,
            )
        ## updaing parent's name
        EvaluateTargetPageHandler.update_parent_info(state_data, going_to)
        return going_to

    @staticmethod
    def from_text(
        state_data: StateData,
        user: Optional[User],
        parent_page: Page,
        variables: Dict[str, Variable],
    ) -> str:
        ## evaluating which page should be represented next
        going_to = parent_page.name
        if parent_page.flow and parent_page.flow.text:
            going_to = ConditionalPropositionEvaluator.eval(
                propositions=parent_page.flow.text.fn,
                variables=variables,
                state_data=state_data,
                user=user,
            )
        ## update parent's name
        EvaluateTargetPageHandler.update_parent_info(state_data, going_to)
        return going_to

    @staticmethod
    def update_parent_info(state_data: StateData, target_page: str):
        if state_data.name != target_page:
            state_data.parent.name = state_data.name
        state_data.name = target_page
