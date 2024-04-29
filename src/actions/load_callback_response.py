from src.models.page.callback_box import CallbackBox
import json


class LoadCallbackResponse:
    @staticmethod
    def from_string(data: str) -> CallbackBox:
        json_file = json.loads(data)
        return CallbackBox(**json_file)
