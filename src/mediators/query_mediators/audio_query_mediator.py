from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
from telegram import File, Update
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
class AudioQueryMediator(QueryMediator):
    file: Optional[File] = None

    @classmethod
    async def build(
        cls, update: Update, context: ContextTypes.DEFAULT_TYPE, repository: Repository
    ) -> AudioQueryMediator:
        state_data = StateDataCrafter.from_context(context)
        file = None
        if update.message and update.message.voice:
            ## voice message
            file = await update.message.voice.get_file()
        elif update.message and update.message.audio:
            ## audio file
            file = await update.message.audio.get_file()

        return cls(
            repository=repository,
            file=file,
            state_data=state_data,
            update=update,
            entry_type=FlowTypes.AUDIO,
        )

    def initialize_chain(self, variables: Dict[str, Variable]) -> AudioQueryMediator:
        """Store parent variable,
        Detect which state are we in,
        Detect which state we are heading to, and
        Update parent's info
        """
        ## detect parent page
        parent_page = self.detect_page().page
        StoreVariableHandler.store_audio(self.state_data, self.file, parent_page)
        EvaluateTargetPageHandler.with_flow(
            flow=FlowFinder.with_page(parent_page, FlowTypes.AUDIO),
            user=self.update.effective_user,
            state_data=self.state_data,
            variables=variables,
            default=parent_page.name,
        )
        ## set the response type
        self.state_data.response_type = ResponseTypes.MESSAGE
        return self
