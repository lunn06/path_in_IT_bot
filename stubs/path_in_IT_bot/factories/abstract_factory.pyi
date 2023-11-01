from abc import ABC
from typing import Any, Iterable

class AbstractFactory(ABC):
    @property
    def items(self) -> Iterable[Any]: ...
