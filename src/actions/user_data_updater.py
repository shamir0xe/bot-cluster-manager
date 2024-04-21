from telegram.ext import ContextTypes
from src.models.state_data import StateData


class UserDataUpdater:
    @staticmethod
    def update(context: ContextTypes.DEFAULT_TYPE, state_data: StateData):
        if isinstance(context.user_data, dict):
            print("here")
            for key, value in state_data.model_dump().items():
                print(f"{key} = {value}")
                context.user_data[key] = value
