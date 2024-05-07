from __future__ import annotations

from aiogram.fsm.state import StatesGroup, State  # noqa: F401

from bot.templates import meta_class_env
from bot.utils import random_str


class StatesGroupBuilder:
    _states: list[str]

    def __init__(self, *states: str) -> None:
        if states == ():
            raise ValueError("StatesGroupBuilder has no arguments")
        else:
            self._states: list[str] = list(states)

    def add_states(self, *states) -> StatesGroupBuilder:
        self._states.extend(states)

        return self

    def remove_state(self, target: str) -> StatesGroupBuilder:
        try:
            self._states.remove(target)
        except ValueError:
            pass

        return self

    def build(self) -> type[StatesGroup]:
        t = meta_class_env
        uuid = random_str(5)
        render = t.render(states=self._states, class_id=uuid)
        exec(render)

        return eval(f"Meta_{uuid}")


if __name__ == "__main__":
    res = StatesGroupBuilder("a") \
        .add_states("b", "c") \
        .build()
    print(dir(res))
    print(type(res))
    print(res)
