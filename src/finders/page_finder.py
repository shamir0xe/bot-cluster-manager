from src.helpers.config.config import Config
from src.models.state_data import StateData
from src.models.page import Page


class PageFinder:
    @staticmethod
    def with_state(state_data: StateData) -> Page:
        data = Config(
            base_folder=f"src.bots.bot_{state_data.bot_id}.configs",
        ).read("scenario.pages")
        for page_data in data:
            if page_data["name"] == state_data.name:
                return Page(**page_data)
        raise Exception("No such page found")
