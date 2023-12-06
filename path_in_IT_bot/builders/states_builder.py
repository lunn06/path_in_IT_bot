from typing import override

from aiogram.fsm.state import StatesGroup, State  # noqa: F401

from path_in_IT_bot.utils import random_str
from path_in_IT_bot.templates import meta_class_env
from path_in_IT_bot.builders.abstract_builder import AbstractBuilder


class StatesGroupBuilder(AbstractBuilder):
    _product: type[StatesGroup]

    def __init__(self, *states: str) -> None:
        self._states: list[str] = list(states)

    @override
    @property
    def product(self) -> type[StatesGroup]:
        return self._product

    @staticmethod
    @override
    def build_from(*entities: str) -> type[StatesGroup]:
        builder = StatesGroupBuilder(*entities)
        builder.produce()

        return builder.product

    def add(self, *states) -> None:
        self._states.extend(states)

    def remove(self, target: str) -> None:
        if target in self._states:
            self._states.remove(target)

    @override
    def produce(self) -> None:
        states: list[str] = self._states

        t = meta_class_env
        uuid = random_str(5)
        render = t.render(states=states, class_id=uuid)
        exec(render)

        self._product = eval(f"Meta_{uuid}")


if __name__ == "__main__":
    res = StatesGroupBuilder.build_from(*["a", "b", "c"])
    print(dir(res))
    print(type(res))
    print(res)
