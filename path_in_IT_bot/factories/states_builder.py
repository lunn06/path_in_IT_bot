from typing import Iterable, Type

from aiogram.fsm.state import State, StatesGroup


class StatesGroupBuilder:
    def __init__(self, *states: Iterable[str]):
        self._states: list[str] = list(*states)

    def add(self, *states) -> None:
        self._states.extend(states)

    def build(self) -> Type[StatesGroup]:
        states: list[str] = self._states

        class Meta(StatesGroup):
            @classmethod
            def insert_states(cls):
                for state_name in states:
                    state = State(state=state_name)
                    state._group = cls
                    setattr(cls, state_name, state)

        Meta.insert_states()
        return Meta
