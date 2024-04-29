from pydantic import BaseModel


class CallbackBox(BaseModel):
    p: str = ""
    b: str = ""
