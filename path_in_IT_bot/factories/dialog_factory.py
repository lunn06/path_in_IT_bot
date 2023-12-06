from aiogram.fsm.state import StatesGroup
from aiogram_dialog import Dialog

from path_in_IT_bot.builders.dialogs_builder import DialogsBuilder
from path_in_IT_bot.builders.states_builder import StatesGroupBuilder
from path_in_IT_bot.entities.graph import AbstractNode
from path_in_IT_bot.entities.interveiw import Interview
from path_in_IT_bot.factories.abstract_factory import AbstractFactory
from path_in_IT_bot.factories.interviews_factory import InterviewsFactory
from path_in_IT_bot.utils import iter_graph


class DialogFactoryItem:
    name: str
    root: AbstractNode
    states: type[StatesGroup]
    dialog: Dialog

    def __init__(self, name: str, root: AbstractNode, states_group: type[StatesGroup], dialog: Dialog):
        self.name = name
        self.root = root
        self.states = states_group
        self.dialog = dialog


class DialogFactory(AbstractFactory):
    _interviews: list[Interview]

    def __init__(self, interviews_path: str):
        interviews_factory = InterviewsFactory(interviews_path)
        self._interviews = interviews_factory.items
        self._items = []

        for interview in self._interviews:
            states_group = DialogFactory.generate_state(interview)
            dialog = DialogsBuilder.build_from(interview, states_group)

            self._items += [
                DialogFactoryItem(
                    interview.name,
                    interview.root,
                    states_group,
                    dialog,
                )]

    @staticmethod
    def generate_state(interview) -> type[StatesGroup]:
        return StatesGroupBuilder.build_from(*[node.id for node in iter_graph(interview.root)])


if __name__ == "__main__":
    factory = DialogFactory("/home/dcdnc/mycod/python/path_in_IT_bot/models/interviews")
    for item in factory.items:
        print(item)
