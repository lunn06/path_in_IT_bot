from abc import ABC
from typing import Iterable, Any


class AbstractFactory(ABC):
    @property
    def items(self) -> Iterable[Any]:
        raise NotImplemented
