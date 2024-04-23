from typing import Optional
from pydantic import BaseModel

from src.models.input_flow import InputFlow


class PageFlow(BaseModel):
    text: Optional[InputFlow] = None
    video: Optional[InputFlow] = None
    photo: Optional[InputFlow] = None
    location: Optional[InputFlow] = None
