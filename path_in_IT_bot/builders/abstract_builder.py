from abc import ABC, abstractmethod
from typing import Any


class AbstractBuilder(ABC):
    _product: Any

    @property
    @abstractmethod
    def product(self) -> Any:
        return self._product

    @abstractmethod
    def produce(self) -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def build_from(*args, **kwargs) -> Any:
        raise NotImplementedError()
