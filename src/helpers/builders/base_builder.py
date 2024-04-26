from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class BaseBuilder(ABC, Generic[T]):
    @abstractmethod
    def build(self, *args, **kwargs) -> T:
        pass

