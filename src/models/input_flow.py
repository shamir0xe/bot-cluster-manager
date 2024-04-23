from typing import List, Optional
from pydantic import BaseModel, Field

from src.models.conditional_proposition import ConditionalProposition


class InputFlow(BaseModel):
    name: Optional[str] = None
    fn: List[ConditionalProposition] = Field(default_factory=list)
