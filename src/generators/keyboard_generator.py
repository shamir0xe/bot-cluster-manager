from __future__ import annotations

from telegram import InlineKeyboardMarkup
from generators.base_generator import BaseGenerator
from models.state import State


class KeyboardGenerator(BaseGenerator):
    @classmethod
    def with_state(cls, state: State) -> KeyboardGenerator:
        # TODO
        generator = cls()
        return generator

    def generate(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([])
