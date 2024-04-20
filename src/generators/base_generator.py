from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar('T')

class BaseGenerator(ABC, Generic[T]):
    @abstractmethod
    def generate(self) -> T:
        pass

