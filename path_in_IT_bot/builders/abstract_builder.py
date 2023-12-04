from abc import ABC, abstractmethod


class AbstractBuilder(ABC):
    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def produce(self) -> None:
        pass
