from typing import List, Optional
from pydantic import BaseModel
from src.models.conditional_proposition import ConditionalProposition


class PageFlow(BaseModel):
    text: Optional[List[ConditionalProposition]] = None
    video: Optional[List[ConditionalProposition]] = None
    audio: Optional[List[ConditionalProposition]] = None
    photo: Optional[List[ConditionalProposition]] = None
    location: Optional[List[ConditionalProposition]] = None
