from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
from telegram import User
from src.models.page import Page
from src.finders.page_finder import PageFinder
from src.actions.apply_variables import ApplyVariables
from src.generators.base_generator import BaseGenerator
from src.helpers.config.config import Config
from src.models.state_data import StateData
from src.types.variable import Variable


@dataclass
class ContentGenerator(BaseGenerator):
    page: Page
    state_data: StateData
    variables: Dict[str, Variable]
    user: Optional[User] = None
    template: str = ""
    content: str = ""

    @classmethod
    def with_state(
        cls,
        state_data: StateData,
        page: Page,
        variables: Dict[str, Variable],
        user: Optional[User],
    ) -> ContentGenerator:
        return cls(page, state_data, variables, user)

    def fetch_template(self) -> ContentGenerator:
        ## Call database in production instead of reading json
        # self.template = self.page.content
        # self.template = Config(
        #     base_folder=f"src.bots.bot_{self.bot_id}.configs",
        # ).read(f"scenario.states.__{self.state_id}.content")
        return self

    def apply_variables(self) -> ContentGenerator:
        ## Search and replace the variables with global scope
        self.content = ApplyVariables.with_content(
            variables=self.variables,
            template=self.page.content,
            state_data=self.state_data,
            user=self.user,
        )

        return self

    def call_bot_specific_handler(self) -> ContentGenerator:
        ## TODO - Implement bot-specific handler for handling content
        ## on bot's desire way
        return self

    def generate(self) -> str:
        # self.fetch_template()
        self.apply_variables()
        self.call_bot_specific_handler()
        return self.content
