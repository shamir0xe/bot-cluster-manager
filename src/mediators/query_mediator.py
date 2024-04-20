from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.actions.answer_callback import AnswerCallback
from src.actions.message_edit import MessageEdit
from src.actions.message_reply import MessageReply
from src.generators.content_generator import ContentGenerator
from src.generators.keyboard_generator import KeyboardGenerator
from src.models.state import State
from src.models.user_data import UserData
from src.types.entry_types import EntryTypes
from src.types.response_types import ResponseTypes


@dataclass
class QueryMediator:
    state: State
    user_data: UserData
    entry_type: EntryTypes
    update: Update
    content: str = ""
    keyboard: Optional[InlineKeyboardMarkup] = None

    @classmethod
    def from_callback(
        cls, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> QueryMediator:
        user_data = UserData()
        if isinstance(context.user_data, dict):
            user_data = UserData(**context.user_data)

        mediator = cls(
            state=State.build_with(bot_id=6, state_id=user_data.state_id),
            user_data=user_data,
            update=update,
            entry_type=EntryTypes.CALLBACK,
        )
        return mediator

    def validate_data(self) -> QueryMediator:
        ## Validate the returned result
        return self

    def map_data(self) -> QueryMediator:
        ## Call data mappers to the proper valuse
        return self

    def store_data(self) -> QueryMediator:
        ## Save data as ...
        return self

    def create_content(self) -> QueryMediator:
        ## Creating the display content based on the state and user_data
        self.content = ContentGenerator.with_state(
            self.state, user_data=self.user_data
        ).generate()
        return self

    def create_keyboard(self) -> QueryMediator:
        ## Deciding each function to do what
        self.keyboard = KeyboardGenerator.with_state(self.state).generate()
        return self

    async def answer(self) -> QueryMediator:
        if self.entry_type is EntryTypes.CALLBACK:
            await AnswerCallback.with_update(self.update)
        response_type = self.state.response_type
        if response_type is ResponseTypes.EDIT_TEXT:
            await MessageEdit.with_update(
                self.update, text=self.content, keyboard=self.keyboard
            )
        elif response_type is ResponseTypes.MESSAGE:
            await MessageReply.with_update(
                self.update, text=self.content, keyboard=self.keyboard
            )

        return self
