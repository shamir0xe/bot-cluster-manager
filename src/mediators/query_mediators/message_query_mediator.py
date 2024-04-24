from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from telegram import Update
from telegram.ext import ContextTypes
from src.actions.handlers.evaluate_target_page_handler import EvaluateTargetPageHandler
from src.actions.handlers.store_variable_handler import StoreVariableHandler
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

    def initialize_chain(self, variables: Dict[str, Variable]) -> MessageQueryMediator:
        """Store parent variable,
        Detect which state are we in,
        Detect which state we are heading to, and
        Update parent's info
        """
        parent_page = self.detect_page().page
        StoreVariableHandler.store_text(self.state_data, self.input, parent_page)
        EvaluateTargetPageHandler.from_text(
            self.state_data, self.update.effective_user, parent_page, variables
        )
        ## set the response type
        self.state_data.response_type = ResponseTypes.MESSAGE
        return self
