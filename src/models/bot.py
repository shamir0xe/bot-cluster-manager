from pydantic import BaseModel


class Bot(BaseModel):
    id: int
    token: str
    name: str
