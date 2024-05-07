from abc import ABC
from typing import Any


class AbstractFactory(ABC):
    _items: list[Any]

    @property
    def items(self) -> list[Any]:
        return self._items
