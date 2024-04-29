from typing import Optional
from telegram import File
from src.models.page.page import Page
from src.models.utility.state_data import StateData
from src.types.flow_types import FlowTypes


class StoreVariableHandler:
    """Store variables from the last page and update parent's data"""

    @staticmethod
    def store_photo(state_data: StateData, file: Optional[File], parent_page: Page):
        ## store
        photo_variable = f"{parent_page.name}_photo"
        if file:
            state_data.variables[photo_variable] = file.file_id
        ## updating parent data
        state_data.parent.flow_type = FlowTypes.PHOTO

    @staticmethod
    def store_video(state_data: StateData, file: Optional[File], parent_page: Page):
        ## store
        video_variable = f"{parent_page.name}_video"
        if file:
            state_data.variables[video_variable] = file.file_id
        ## updating parent data
        state_data.parent.flow_type = FlowTypes.VIDEO

    @staticmethod
    def store_audio(state_data: StateData, file: Optional[File], parent_page: Page):
        ## store
        audio_var = f"{parent_page.name}_audio"
        if file:
            state_data.variables[audio_var] = file.file_id
        ## updating parent data
        state_data.parent.flow_type = FlowTypes.AUDIO

    @staticmethod
    def store_text(state_data: StateData, input_text: str, parent_page: Page):
        ## store the input_text to the state_data.variables[variable]
        input_variable = f"{parent_page.name}_text"
        state_data.variables[input_variable] = input_text
        ## updating parent data
        state_data.parent.flow_type = FlowTypes.TEXT
