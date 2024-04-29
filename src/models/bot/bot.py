from typing import Annotated
from pydantic import BaseModel, BeforeValidator

AnnotatedInt = Annotated[int, BeforeValidator(lambda id: int(id))]


class Bot(BaseModel):
    id: AnnotatedInt
    token: str
    name: str
