from __future__ import annotations

from telegram import InlineKeyboardMarkup
from src.models.keyboard import Keyboard
from src.models.state_data import StateData
from src.generators.base_generator import BaseGenerator


class KeyboardGenerator(BaseGenerator):
    @classmethod
    def with_state(cls, state_data: StateData, keyboard_data: Keyboard) -> KeyboardGenerator:
        # TODO
        generator = cls()
        return generator

    def evaluate_functions(self) -> KeyboardGenerator:
        return self

    def generate(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([])
