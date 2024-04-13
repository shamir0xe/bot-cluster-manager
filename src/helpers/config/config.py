from typing import Any
from pylib_0xe.config.config import Config as CFG


class Config:
    @staticmethod
    def read(selector: str, **kwargs) -> Any:
        config = CFG(file_path=__file__)
        return config.read(selector, **kwargs)
