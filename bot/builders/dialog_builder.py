
from aiogram.fsm.state import StatesGroup
from aiogram_dialog import Dialog, Window

from bot.builders.window_builder import WindowBuilder
from bot.entities.interveiw import Interview
from bot.utils import iter_graph


class DialogBuilder:
    _product: Dialog
    _interview: Interview
    _states_group: type[StatesGroup]

    def __init__(self, interview: Interview, states_group: type[StatesGroup]) -> None:
        self._interview = interview
        self._states_group = states_group

    @property
    def product(self) -> Dialog:
        return self._product

    def produce(self) -> None:
        init_node = self._interview.root

        windows: list[Window] = [
            WindowBuilder.build(node, self._states_group)
            for node in iter_graph(init_node)
        ]
        self._product = Dialog(*windows)

    @staticmethod
    def build(interview: Interview, states_group: type[StatesGroup]) -> Dialog:
        builder = DialogBuilder(interview, states_group)
        builder.produce()

        return builder.product
