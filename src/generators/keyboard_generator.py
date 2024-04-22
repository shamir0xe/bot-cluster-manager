from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, User
from src.actions.conditional_proposition_evaluator import (
    ConditionalPropositionEvaluator,
)
from src.models.keyboard import Keyboard
from src.models.state_data import StateData
from src.generators.base_generator import BaseGenerator
from src.types.variable import Variable


@dataclass
class KeyboardGenerator(BaseGenerator):
    state_data: StateData
    keyboard_data: Keyboard
    user: Optional[User]
    variables: Dict[str, Variable]
    buttons: List[List[InlineKeyboardButton]] = field(default_factory=list)

    def evaluate_layout(self) -> KeyboardGenerator:
        self.buttons = []
        for row_buttons in self.keyboard_data.buttons:
            row: List[InlineKeyboardButton] = []
            for button in row_buttons:
                row += [
                    InlineKeyboardButton(
                        text=button.text,
                        callback_data=ConditionalPropositionEvaluator.eval(
                            button.fn,
                            variables=self.variables,
                            state_data=self.state_data,
                            user=self.user,
                        ),
                    )
                ]
            self.buttons += [row]
        return self

    def generate(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(self.buttons)
