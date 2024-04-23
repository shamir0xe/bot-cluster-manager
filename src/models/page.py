from typing import Optional
from pydantic import BaseModel

from src.models.page_flow import PageFlow
from src.models.keyboard import Keyboard


class Page(BaseModel):
    name: str
    content: str = ""
    keyboard: Keyboard
    flow: Optional[PageFlow] = None

