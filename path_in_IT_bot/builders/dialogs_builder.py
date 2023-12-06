from typing import override

from aiogram.fsm.state import StatesGroup
from aiogram_dialog import Dialog, Window

from path_in_IT_bot.builders.windows_builder import WindowBuilder
from path_in_IT_bot.entities.interveiw import Interview
from path_in_IT_bot.builders.abstract_builder import AbstractBuilder
from path_in_IT_bot.utils import iter_graph


class DialogsBuilder(AbstractBuilder):
    _product: Dialog
    _interview: Interview
    _states_group: type[StatesGroup]

    def __init__(self, interview: Interview, states_group: type[StatesGroup]) -> None:
        self._interview = interview
        self._states_group = states_group

    @override
    @property
    def product(self) -> Dialog:
        return self._product

    @override
    def produce(self) -> None:
        init_node = self._interview.root

        windows: list[Window] = []
        for node in iter_graph(init_node):
            window = WindowBuilder.build_from(node, self._states_group)
            windows += [window]
        self._product = Dialog(*windows)

    @staticmethod
    @override
    def build_from(interview: Interview, states_group: type[StatesGroup]) -> Dialog:
        builder = DialogsBuilder(interview, states_group)
        builder.produce()

        return builder.product
