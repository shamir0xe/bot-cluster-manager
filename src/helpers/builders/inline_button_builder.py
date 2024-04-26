from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict
from telegram import InlineKeyboardButton
from src.helpers.builders.base_builder import BaseBuilder


@dataclass
class InlineButtonBuilder(BaseBuilder):
    data: Dict[str, Any] = field(default_factory=dict)

    def add_text(self, text: str) -> InlineButtonBuilder:
        self.data["text"] = text
        return self

    def add_callback(self, callback_data: str) -> InlineButtonBuilder:
        self.data["callback_data"] = callback_data
        return self

    def add_url(self, url: str) -> InlineButtonBuilder:
        self.data["url"] = url
        return self

    def build(self, *args, **kwargs) -> InlineKeyboardButton:
        return InlineKeyboardButton(**self.data)
