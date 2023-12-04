from abc import ABC
from typing import Iterable, Any


class AbstractFactory(ABC):
    _items: Iterable[Any]

    @property
    def items(self) -> Iterable[Any]:
        return self._items
