from pydantic import BaseModel

from src.models.keyboard import Keyboard


class Page(BaseModel):
    name: str
    content: str = ""
    keyboard: Keyboard

