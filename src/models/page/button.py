from typing import List, Optional
from pydantic import BaseModel, Field

from .conditional_proposition import ConditionalProposition


class Button(BaseModel):
    text: str = "btn"
    fn: List[ConditionalProposition] = Field(default_factory=list)
    url: Optional[str] = None
