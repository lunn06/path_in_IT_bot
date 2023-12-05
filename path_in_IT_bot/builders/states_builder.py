from typing import Type

from aiogram.fsm.state import StatesGroup, State  # noqa: F401

from path_in_IT_bot.templates import meta_class_env
from path_in_IT_bot.utils import random_str


class StatesGroupBuilder:

    def __init__(self, *states: str):
        """

        :type Iterable[str] states: object
        """

        self._states: list[str] = list(states)

    @staticmethod
    def build_from(*entity: str) -> Type[StatesGroup]:
        builder = StatesGroupBuilder(*entity)
        return builder.build()

    def add(self, *states) -> None:
        self._states.extend(states)

    def remove(self, target: str) -> None:
        if target in self._states:
            self._states.remove(target)

    def build(self) -> Type[StatesGroup]:
        states: list[str] = self._states

        t = meta_class_env
        uuid = random_str(5)
        render = t.render(states=states, class_id=uuid)
        exec(render)

        # class Meta(StatesGroup):
        #     @classmethod
        #     def insert_states(cls):
        #         for state_name in states:
        #             state = State(state=state_name)
        #             state._group = cls
        #             setattr(cls, state_name, state)
        #
        # Meta.insert_states()
        # return Meta

        return eval(f"Meta_{uuid}")


if __name__ == "__main__":
    res = StatesGroupBuilder.build_from(*["a", "b", "c"])
    print(dir(res))
    print(type(res))
    print(res)
