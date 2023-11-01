from __future__ import annotations

from typing import Any, Callable

from aiogram.fsm.state import StatesGroup, State

from path_in_IT_bot.readers.model_reader import model


class Menu(StatesGroup):
    main_menu = State()

    @classmethod
    def initialize(cls: type[StatesGroup]) -> None:
        for producer_name in model.producers.keys():
            value = State(state=producer_name)
            value._group = cls
            setattr(cls, producer_name, value)


Menu.initialize()

if __name__ == "__main__":
    print(dir(Menu))  # type: ignore
