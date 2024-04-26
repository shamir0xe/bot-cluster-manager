from src.helpers.config.config import Config
from src.models.env_data import EnvData
from src.helpers.decorators.singleton import singleton
from src.types.repository_types import RepositoryTypes


@singleton
class Env:
    env: EnvData

    def __init__(self) -> None:
        self.env = EnvData(**Config().read("env"))

    @property
    def repository(self) -> RepositoryTypes:
        return self.env.repository

    @property
    def debug(self) -> bool:
        return self.env.debug
