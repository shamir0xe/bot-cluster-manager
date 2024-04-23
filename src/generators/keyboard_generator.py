from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, User
from src.models.callback_box import CallbackBox
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
                        callback_data=CallbackBox(
                            p=ConditionalPropositionEvaluator.eval(
                                button.fn,
                                variables=self.variables,
                                state_data=self.state_data,
                                user=self.user,
                            ),
                            b=button.text,
                        ).model_dump_json(),
                    )
                ]
            self.buttons += [row]
        print()
        print()
        print("buttons are as follows")
        print(self.buttons)
        return self

    def generate(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(self.buttons)
