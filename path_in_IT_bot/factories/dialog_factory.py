from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import Window, DialogManager, Dialog

from path_in_IT_bot.utils import iter_over_graph
from path_in_IT_bot.entities.interveiw import Interview
from path_in_IT_bot.builders.states_builder import StatesGroupBuilder
from path_in_IT_bot.factories.abstract_factory import AbstractFactory
from path_in_IT_bot.factories.interviews_factory import InterviewsFactory
from path_in_IT_bot.entities.graph import AbstractNode, InitNode, EndNode, QuestionNode, YesNoQuestionNode


class NamedDialog(Dialog):
    def __init__(self, name: str, root: AbstractNode, states_group: StatesGroup, *windows):
        super().__init__(*windows)
        self.name = name
        self.root = root
        self.states = states_group


class DialogFactory(AbstractFactory):
    _interviews: list[Interview]

    def __init__(self, interviews_path: str):
        interviews_factory = InterviewsFactory(interviews_path)
        self._interviews = interviews_factory.items
        self._items = []

        for interview in self._interviews:
            states_group = DialogFactory.generate_state(interview)
            init_node = interview.root

            async def button_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
                await manager.next()

            windows = []
            for node in iter_over_graph(init_node):
                match node:
                    case InitNode(id=node.id):
                        window = Window(
                            Const(node.text),
                            Button(Const("Next"), id="button_clicked"),
                            state=getattr(states_group, f"state_{node.id}")
                        )
                    case EndNode(id=node.id):
                        window = Window(
                            Const(node.text),
                            Button(Const("Next"), id="button_clicked"),
                            state=getattr(states_group, f"state_{node.id}")
                        )
                    case YesNoQuestionNode(id=node.id):
                        window = Window(
                            Const(node.text),
                            Button(Const("Next"), id="button_clicked"),
                            state=getattr(states_group, f"state_{node.id}")
                        )
                    case QuestionNode(id=node.id):
                        window = Window(
                            Const(node.text),
                            Button(Const("Next"), id="button_clicked"),
                            state=getattr(states_group, f"state_{node.id}")
                        )
                    case _:
                        raise ValueError()

                windows.append(window)
            self._items.append(NamedDialog(interview.name, interview.root, states_group, *windows))  # type: ignore

    @staticmethod
    def generate_state(interview):
        return StatesGroupBuilder.build_from(*[node.id for node in interview.nodes])


if __name__ == "__main__":
    factory = DialogFactory("/home/dcdnc/mycod/python/path_in_IT_bot/models/interviews")
    for item in factory.items:
        print(item)
