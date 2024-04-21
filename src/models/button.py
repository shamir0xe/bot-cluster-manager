from typing import List
from pydantic import BaseModel, Field

from src.models.conditional_proposition import ConditionalProposition


class Button(BaseModel):
    text: str = "btn"
    fn: List[ConditionalProposition] = Field(default_factory=list)
