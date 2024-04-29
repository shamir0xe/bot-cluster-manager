from typing import List
from pydantic import BaseModel

from .button import Button
from src.types.keyboard_types import KeyboardTypes


class Keyboard(BaseModel):
    type: str = KeyboardTypes.Inline.name
    buttons: List[List[Button]]
