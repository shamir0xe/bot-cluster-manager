from typing import Optional
from pydantic import BaseModel

from .page_flow import PageFlow
from .keyboard import Keyboard


class Page(BaseModel):
    name: str
    content: str = ""
    keyboard: Keyboard
    flow: Optional[PageFlow] = None

