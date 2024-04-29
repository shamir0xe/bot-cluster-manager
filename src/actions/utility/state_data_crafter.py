from telegram.ext import ContextTypes
from src.models.utility.state_data import StateData
from src.types.exception_types import ExceptionTypes


class StateDataCrafter:
    @staticmethod
    def from_context(context: ContextTypes.DEFAULT_TYPE):
        state_data = StateData()
        if isinstance(context.user_data, dict):
            state_data = StateData(**context.user_data)
        if not state_data.started:
            raise Exception(ExceptionTypes.NOT_STARTED)
        return state_data
