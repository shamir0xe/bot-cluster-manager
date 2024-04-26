from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
from telegram import File, Update
from telegram.ext import ContextTypes
from src.repositories.repository import Repository
from src.actions.state_data_crafter import StateDataCrafter
from src.finders.flow_finder import FlowFinder
from src.actions.handlers.evaluate_target_page_handler import EvaluateTargetPageHandler
from src.actions.handlers.store_variable_handler import StoreVariableHandler
from src.mediators.query_mediator import QueryMediator
from src.types.response_types import ResponseTypes
from src.types.variable import Variable
from src.types.flow_types import FlowTypes


@dataclass
class PhotoQueryMediator(QueryMediator):
    file: Optional[File] = None

    @classmethod
    async def build(
        cls, update: Update, context: ContextTypes.DEFAULT_TYPE, repository: Repository
    ) -> PhotoQueryMediator:
        state_data = StateDataCrafter.from_context(context)
        file = None
        if update.message and update.message.photo:
            file = await update.message.photo[-1].get_file()
            file.file_id

        return cls(
            repository=repository,
            file=file,
            state_data=state_data,
            update=update,
            entry_type=FlowTypes.PHOTO,
        )

    def initialize_chain(self, variables: Dict[str, Variable]) -> PhotoQueryMediator:
        """Store parent variable,
        Detect which state are we in,
        Detect which state we are heading to, and
        Update parent's info
        """
        ## detect parent page
        parent_page = self.detect_page().page
        StoreVariableHandler.store_photo(self.state_data, self.file, parent_page)
        EvaluateTargetPageHandler.with_flow(
            flow=FlowFinder.with_page(parent_page, FlowTypes.PHOTO),
            user=self.update.effective_user,
            state_data=self.state_data,
            variables=variables,
            default=parent_page.name,
        )
        ## set the response type
        self.state_data.response_type = ResponseTypes.MESSAGE
        return self
