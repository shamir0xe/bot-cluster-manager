from typing import Annotated, Any
from pydantic import BaseModel, BeforeValidator
from pydantic.networks import IPvAnyNetwork
from src.types.repository_types import RepositoryTypes


def repository_mapper(v: Any):
    if v == "db":
        return RepositoryTypes.DATABASE
    if v == "api":
        return RepositoryTypes.API
    raise ValueError("values must be in [db, api]")


RT = Annotated[RepositoryTypes, BeforeValidator(repository_mapper)]


class EnvData(BaseModel):
    debug: bool
    repository: RT
    port: int
    host: IPvAnyNetwork
