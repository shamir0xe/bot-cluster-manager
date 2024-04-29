from pydantic import BaseModel


class BotCfg(BaseModel):
    id: int
    name: str
    error_message: str
