from typing import List
from pydantic import BaseModel, Field


class ConditionalProposition(BaseModel):
    con: str
    hyp: List[str] = Field(default_factory=list)
