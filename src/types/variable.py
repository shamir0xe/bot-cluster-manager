from abc import ABC, abstractmethod
from dataclasses import dataclass


class Variable(ABC):
    name: str = ""

    def __init_subclass__(cls) -> None:
        if cls.name == "":
            raise NotImplementedError("Subclass must override 'name' attribute")

    @property
    def pattern(self) -> str:
        return f"<:{self.name}>"

    @staticmethod
    @abstractmethod
    def callback(**kwargs) -> str:
        pass

    def __str__(self) -> str:
        return f"variable: {self.__class__}, pattern: {self.pattern}"
