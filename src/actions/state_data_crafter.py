from telegram.ext import ContextTypes

from src.models.state_data import StateData


class StateDataCrafter:
    @staticmethod
    def from_context(context: ContextTypes.DEFAULT_TYPE):
        state_data = StateData()
        if isinstance(context.user_data, dict):
            state_data = StateData(**context.user_data)
        return state_data
