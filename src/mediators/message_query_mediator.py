from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from telegram import Update
from telegram.ext import ContextTypes
from src.models.parent_page import ParentPage
from src.actions.conditional_proposition_evaluator import (
    ConditionalPropositionEvaluator,
)
from src.mediators.query_mediator import QueryMediator
from src.types.entry_types import EntryTypes
from src.types.response_types import ResponseTypes
from src.types.variable import Variable


@dataclass
class MessageQueryMediator(QueryMediator):
    input: str = ""

    @classmethod
    def build(
        cls, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> MessageQueryMediator:
        state_data = cls.craft_state_data(context)
        input = ""
        if update.message and update.message.text:
            input = update.message.text
            ## modeli ke baayad javaab bargardoonim
            state_data.response_type = ResponseTypes.MESSAGE

        return cls(
            input=input,
            state_data=state_data,
            update=update,
            entry_type=EntryTypes.MESSAGE,
        )

    def craft_state(self, variables: Dict[str, Variable]) -> MessageQueryMediator:
        parent_page = self.detect_page().page

        ## store the input to the state_data.variables[variable]
        input_variable = f"{parent_page.name}_text"
        if parent_page.flow and parent_page.flow.text and parent_page.flow.text.name:
            input_variable = parent_page.flow.text.name
        self.state_data.variables[input_variable] = self.input

        ## updating parent data
        self.state_data.parent.response_type = ResponseTypes.MESSAGE

        ## evaluating which page should be represented next
        going_to = parent_page.name
        if parent_page.flow and parent_page.flow.text:
            going_to = ConditionalPropositionEvaluator.eval(
                propositions=parent_page.flow.text.fn,
                variables=variables,
                state_data=self.state_data,
                user=self.update.effective_user,
            )
        ## update parent's name
        if self.state_data.name != going_to:
            self.state_data.parent.name = self.state_data.name
        self.state_data.name = going_to

        print(f"going to {going_to}")
        return self
