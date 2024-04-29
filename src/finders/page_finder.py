from src.repositories.repository import Repository
from src.models.utility.state_data import StateData
from src.models.page.page import Page
from src.types.exception_types import ExceptionTypes


class PageFinder:
    @staticmethod
    def with_state(state_data: StateData, repository: Repository) -> Page:
        pages = repository.get_pages(state_data.bot_id)
        for page in pages:
            if page.name == state_data.name:
                return page
        raise Exception(ExceptionTypes.PAGE_NOT_FOUND)
