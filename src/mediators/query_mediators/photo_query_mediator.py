from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
from telegram import File, Update
from telegram.ext import ContextTypes
from src.actions.handlers.evaluate_target_page_handler import EvaluateTargetPageHandler
from src.actions.handlers.store_variable_handler import StoreVariableHandler
from src.mediators.query_mediator import QueryMediator
from src.types.entry_types import EntryTypes
from src.types.response_types import ResponseTypes
from src.types.variable import Variable


@dataclass
class PhotoQueryMediator(QueryMediator):
    file: Optional[File] = None

    @classmethod
    async def build(
        cls, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> PhotoQueryMediator:
        state_data = cls.craft_state_data(context)
        file = None
        if update.message and update.message.photo:
            file = await update.message.photo[-1].get_file()
            file.file_id

        return cls(
            file=file, state_data=state_data, update=update, entry_type=EntryTypes.PHOTO
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
        EvaluateTargetPageHandler.from_photo(
            self.state_data, self.update.effective_user, parent_page, variables
        )
        ## set the response type
        self.state_data.response_type = ResponseTypes.MESSAGE
        return self
