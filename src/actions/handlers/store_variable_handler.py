from typing import Optional
from telegram import File
from src.models.page import Page
from src.models.state_data import StateData
from src.types.response_types import ResponseTypes


class StoreVariableHandler:
    """Store variables from the last page and update parent's data"""

    @staticmethod
    def store_photo(state_data: StateData, file: Optional[File], parent_page: Page):
        ## store
        photo_variable = f"{parent_page.name}_img"
        if parent_page.flow and parent_page.flow.photo and parent_page.flow.photo.name:
            photo_variable = parent_page.flow.photo.name
        if file:
            state_data.variables[photo_variable] = file.file_id
        ## updating parent data
        state_data.parent.response_type = ResponseTypes.PHOTO

    @staticmethod
    def store_text(state_data: StateData, input_text: str, parent_page: Page):
        ## store the input_text to the state_data.variables[variable]
        input_variable = f"{parent_page.name}_text"
        if parent_page.flow and parent_page.flow.text and parent_page.flow.text.name:
            input_variable = parent_page.flow.text.name
        state_data.variables[input_variable] = input_text
        ## updating parent data
        state_data.parent.response_type = ResponseTypes.MESSAGE
