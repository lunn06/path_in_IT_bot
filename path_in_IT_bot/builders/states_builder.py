from typing import Iterable, Type

from aiogram.fsm.state import State, StatesGroup


class StatesGroupBuilder:

    def __init__(self, *states: Iterable[str]):
        self._states: list[str] = list(states)

    @staticmethod
    def build_from(entity: Iterable[str]) -> Type[StatesGroup]:
        builder = StatesGroupBuilder(*entity)
        return builder.build()

    def add(self, *states) -> None:
        self._states.extend(states)

    def remove(self, target: str) -> None:
        if target in self._states:
            self._states.remove(target)

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
