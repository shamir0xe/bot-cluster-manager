from __future__ import annotations
from dataclasses import dataclass
from generators.base_generator import BaseGenerator
from models.state import State
from models.user_data import UserData


@dataclass
class ContentGenerator(BaseGenerator):
    @classmethod
    def with_state(cls, state: State, user_data: UserData) -> ContentGenerator:
        # TODO
        generator = cls(state, user_data.data)
        return generator

    def generate(self) -> str:
        return ""
