from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Variable(ABC):
    pattern: str = ""

    def __init_subclass__(cls) -> None:
        if not cls.pattern:
            raise NotImplementedError("Subclass must override 'name' attribute")

    @staticmethod
    @abstractmethod
    def callback(**kwargs) -> str:
        pass

