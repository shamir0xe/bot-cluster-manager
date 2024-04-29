from src.models.utility.credentials import Credentials
from src.models.utility.api import API
from src.helpers.config.config import Config
from src.models.utility.env_data import EnvData
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

    @property
    def api(self) -> API:
        return self.env.api

    @property
    def credentials(self) -> Credentials:
        return self.env.api.credentials
