from typing import Dict

from pydantic import BaseModel
from src.types.query_types import QueryTypes


class QueryWrapper(BaseModel):
    name: QueryTypes
    response_field: str
    query: Dict
