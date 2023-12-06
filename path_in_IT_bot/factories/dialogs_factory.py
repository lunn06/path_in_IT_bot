from aiogram.fsm.state import StatesGroup
from aiogram_dialog import Dialog

from path_in_IT_bot.builders.dialog_builder import DialogBuilder
from path_in_IT_bot.builders.states_group_builder import StatesGroupBuilder
from path_in_IT_bot.entities.graph import InitNode
from path_in_IT_bot.entities.interveiw import Interview
from path_in_IT_bot.factories.abstract_factory import AbstractFactory
from path_in_IT_bot.factories.interviews_factory import InterviewsFactory
from path_in_IT_bot.utils import iter_graph


class DialogsFactoryItem:
    _name: str
    _root: InitNode
    _states: type[StatesGroup]
    _dialog: Dialog

    def __init__(self, name: str, root: InitNode, states_group: type[StatesGroup], dialog: Dialog):
        self._name = name
        self._root = root
        self._states = states_group
        self._dialog = dialog

    @property
    def name(self) -> str:
        return self._name

    @property
    def root(self) -> InitNode:
        return self._root

    @property
    def states(self) -> type[StatesGroup]:
        return self._states

    @property
    def dialog(self) -> Dialog:
        return self._dialog


class DialogsFactory(AbstractFactory):
    _items: list[DialogsFactoryItem]
    _interviews: list[Interview]

    def __init__(self, interviews_path: str):
        interviews_factory = InterviewsFactory(interviews_path)
        self._interviews = interviews_factory.items
        self._items = []

        for interview in self._interviews:
            states_group = DialogsFactory.generate_state(interview)
            dialog = DialogBuilder.build_from(interview, states_group)

            self._items += [
                DialogsFactoryItem(
                    interview.name,
                    interview.root,
                    states_group,
                    dialog,
                )]

    @staticmethod
    def generate_state(interview) -> type[StatesGroup]:
        return StatesGroupBuilder.build_from(*[node.id for node in iter_graph(interview.root)])


if __name__ == "__main__":
    factory = DialogsFactory("/home/dcdnc/mycod/python/path_in_IT_bot/models/interviews")
    for item in factory.items:
        print(item)
