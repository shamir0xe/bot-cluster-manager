from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from telegram import Update
from telegram.ext import ContextTypes
from src.repositories.repository import Repository
from src.actions.utility.state_data_crafter import StateDataCrafter
from src.finders.flow_finder import FlowFinder
from src.actions.page.evaluate_target_page_handler import EvaluateTargetPageHandler
from src.actions.variable.store_variable_handler import StoreVariableHandler
from src.mediators.query_mediator import QueryMediator
from src.types.response_types import ResponseTypes
from src.types.variable import Variable
from src.types.flow_types import FlowTypes


@dataclass
class TextQueryMediator(QueryMediator):
    input_text: str = ""

    @classmethod
    def build(
        cls, update: Update, context: ContextTypes.DEFAULT_TYPE, repository: Repository
    ) -> TextQueryMediator:
        state_data = StateDataCrafter.from_context(context)
        input_text = ""
        if update.message and update.message.text:
            input_text = update.message.text

        return cls(
            repository=repository,
            input_text=input_text,
            state_data=state_data,
            update=update,
            entry_type=FlowTypes.TEXT,
        )

    def initialize_chain(self, variables: Dict[str, Variable]) -> TextQueryMediator:
        """Store parent variable,
        Detect which state are we in,
        Detect which state we are heading to, and
        Update parent's info
        """
        parent_page = self.detect_page().page
        StoreVariableHandler.store_text(self.state_data, self.input_text, parent_page)
        EvaluateTargetPageHandler.with_flow(
            flow=FlowFinder.with_page(parent_page, FlowTypes.TEXT),
            user=self.update.effective_user,
            state_data=self.state_data,
            variables=variables,
            default=parent_page.name,
        )
        ## set the response type
        self.state_data.response_type = ResponseTypes.MESSAGE
        return self
