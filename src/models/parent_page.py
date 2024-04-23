from pydantic import BaseModel

from src.types.response_types import ResponseTypes


class ParentPage(BaseModel):
    name: str = ""
    response_type: ResponseTypes = ResponseTypes.MESSAGE
