from pydantic import BaseModel

from src.types.flow_types import FlowTypes


class ParentPage(BaseModel):
    name: str = ""
    flow_type: FlowTypes = FlowTypes.CALLBACK
