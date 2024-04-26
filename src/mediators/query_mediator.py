from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.repositories.repository import Repository
from src.actions.state_data_crafter import StateDataCrafter
from src.actions.load_callback_response import LoadCallbackResponse
from src.finders.page_finder import PageFinder
from src.actions.user_data_updater import UserDataUpdater
from src.actions.answer_callback import AnswerCallback
from src.actions.message_edit import MessageEdit
from src.actions.message_reply import MessageReply
from src.generators.content_generator import ContentGenerator
from src.generators.keyboard_generator import KeyboardGenerator
from src.models.state_data import StateData
from src.types.response_types import ResponseTypes
from src.types.variable import Variable
from src.types.flow_types import FlowTypes


@dataclass
class QueryMediator:
    repository: Repository
    state_data: StateData
    entry_type: FlowTypes
    update: Update
    content: str = ""
    keyboard: Optional[InlineKeyboardMarkup] = None

    @classmethod
    def from_command(
        cls, update: Update, context: ContextTypes.DEFAULT_TYPE, repository: Repository
    ) -> QueryMediator:
        state_data = StateDataCrafter.from_context(context)
        state_data.response_type = ResponseTypes.MESSAGE
        mediator = cls(
            repository=repository,
            state_data=state_data,
            update=update,
            entry_type=FlowTypes.COMMAND,
        )
        return mediator

    @classmethod
    def from_callback(
        cls, update: Update, context: ContextTypes.DEFAULT_TYPE, repository: Repository
    ) -> QueryMediator:
        state_data = StateDataCrafter.from_context(context)
        if update.callback_query and update.callback_query.data:
            callback_box = LoadCallbackResponse.from_string(update.callback_query.data)
            ## store the made decision
            state_data.decisions[state_data.name] = callback_box.b
            ## update parent's name
            if state_data.name != callback_box.p:
                state_data.parent.name = state_data.name
            ## updating which state we're heading to
            state_data.name = callback_box.p
            ## set the response type
            state_data.response_type = ResponseTypes.EDIT_TEXT

        mediator = cls(
            repository=repository,
            state_data=state_data,
            update=update,
            entry_type=FlowTypes.CALLBACK,
        )
        return mediator

    def detect_page(self) -> QueryMediator:
        self.page = PageFinder.with_state(self.state_data, self.repository)
        return self

    def validate_data(self) -> QueryMediator:
        ## Validate the returned result
        return self

    def map_data(self) -> QueryMediator:
        ## Call data mappers to the proper valuse
        return self

    def store_data(self) -> QueryMediator:
        ## Save data as ...
        return self

    def create_content(self, variables: Dict[str, Variable]) -> QueryMediator:
        ## Creating the display content based on the state and user_data
        self.content = ContentGenerator.with_state(
            state_data=self.state_data,
            page=self.page,
            variables=variables,
            user=self.update.effective_user,
        ).generate()
        return self

    def create_keyboard(self, variables: Dict[str, Variable]) -> QueryMediator:
        ## Deciding each function to do what
        self.keyboard = (
            KeyboardGenerator(
                state_data=self.state_data,
                keyboard_data=self.page.keyboard,
                user=self.update.effective_user,
                variables=variables,
            )
            .evaluate_layout()
            .generate()
        )
        return self

    async def answer(self) -> QueryMediator:
        if self.entry_type is FlowTypes.CALLBACK:
            await AnswerCallback.with_update(self.update)
        response_type = self.state_data.response_type
        if response_type is ResponseTypes.EDIT_TEXT:
            await MessageEdit.with_update(
                self.update, text=self.content, keyboard=self.keyboard
            )
        elif response_type is ResponseTypes.MESSAGE:
            await MessageReply.with_update(
                self.update, text=self.content, keyboard=self.keyboard
            )

        return self

    def update_user_data(self, context: ContextTypes.DEFAULT_TYPE) -> QueryMediator:
        UserDataUpdater.update(context, self.state_data)
        return self
