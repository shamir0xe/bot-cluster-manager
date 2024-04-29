from src.helpers.config.config import Config
from src.helpers.decorators.singleton import singleton
from src.models.utility.network_config_data import NetworkConfigData


@singleton
class NetworkConfig:
    def __init__(self) -> None:
        self.cfg = NetworkConfigData(**Config().read("network_config"))

    @property
    def max_retries(self) -> int:
        return self.cfg.max_retries

    @property
    def max_errors(self) -> int:
        return self.cfg.max_errors

    @property
    def sleep_interval(self) -> float:
        return self.cfg.sleep_interval
