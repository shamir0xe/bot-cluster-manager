from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.actions.load_callback_response import LoadCallbackResponse
from src.models.parent_page import ParentPage
from src.finders.page_finder import PageFinder
from src.actions.user_data_updater import UserDataUpdater
from src.actions.answer_callback import AnswerCallback
from src.actions.message_edit import MessageEdit
from src.actions.message_reply import MessageReply
from src.generators.content_generator import ContentGenerator
from src.generators.keyboard_generator import KeyboardGenerator
from src.models.state_data import StateData
from src.types.entry_types import EntryTypes
from src.types.response_types import ResponseTypes
from src.types.variable import Variable


@dataclass
class QueryMediator:
    state_data: StateData
    entry_type: EntryTypes
    update: Update
    content: str = ""
    keyboard: Optional[InlineKeyboardMarkup] = None

    @classmethod
    def from_command(
        cls, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> QueryMediator:
        state_data = cls.craft_state_data(context)
        mediator = cls(
            state_data=state_data,
            entry_type=EntryTypes.COMMAND,
            update=update,
        )
        return mediator

    @classmethod
    def from_callback(
        cls, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> QueryMediator:
        state_data = cls.craft_state_data(context)
        if update.callback_query and update.callback_query.data:
            callback_box = LoadCallbackResponse.from_string(update.callback_query.data)
            state_data.decisions[state_data.name] = callback_box.b
            ## update parent's name
            if state_data.name != callback_box.p:
                state_data.parent.name = state_data.name

            ## updating which state we're heading to
            state_data.name = callback_box.p
            state_data.response_type = ResponseTypes.EDIT_TEXT

        mediator = cls(
            state_data=state_data,
            update=update,
            entry_type=EntryTypes.CALLBACK,
        )
        return mediator

    @staticmethod
    def craft_state_data(context: ContextTypes.DEFAULT_TYPE) -> StateData:
        state_data = StateData()
        if isinstance(context.user_data, dict):
            state_data = StateData(**context.user_data)
        return state_data

    def detect_page(self) -> QueryMediator:
        self.page = PageFinder.with_state(self.state_data)
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
        if self.entry_type is EntryTypes.CALLBACK:
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
