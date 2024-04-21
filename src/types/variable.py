from abc import ABC, abstractmethod
from dataclasses import dataclass


class Variable(ABC):
    pattern: str = ""

    def __init_subclass__(cls) -> None:
        if cls.pattern == "":
            raise NotImplementedError("Subclass must override 'name' attribute")

    @staticmethod
    @abstractmethod
    def callback(**kwargs) -> str:
        pass

    def __str__(self) -> str:
        return f"variable: {self.__class__}, pattern: {self.pattern}"

