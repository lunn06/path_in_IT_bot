from typing import Any

from aiogram.fsm.state import StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog import Window, Dialog, DialogManager, ChatEvent

from path_in_IT_bot.utils import iter_graph
from path_in_IT_bot.entities.interveiw import Interview
from path_in_IT_bot.builders.states_builder import StatesGroupBuilder
from path_in_IT_bot.factories.abstract_factory import AbstractFactory
from path_in_IT_bot.factories.interviews_factory import InterviewsFactory
from path_in_IT_bot.entities.graph import AbstractNode, InitNode, EndNode, QuestionNode, ChoseQuestionNode

FINISHED_KEY = "finished"


async def button_end_clicked(callback: CallbackQuery, buttton: Button, manager: DialogManager):
    await manager.done()


async def button_select_clicked(
        callback: ChatEvent,
        select: Any,
        manager: DialogManager,
        item_id: str
):
    ans_node_id, ans = item_id.split("::")
    item: DialogFactoryItem = manager.start_data

    print(manager.current_context().state.__name__)

    for node in iter_graph(item.root):
        if node.id != ans_node_id:
            continue
        manager.dialog_data[node.tags["field"]] = ans
        for branch in node.branches:
            if branch.label == ans:
                await manager.switch_to(getattr(item.states, f"state_{branch.to_node.id}"))


async def next_or_end(callback: CallbackQuery, widget, manager: DialogManager, *_):
    if manager.dialog_data.get(FINISHED_KEY):
        await manager.done()
    else:
        await manager.next()


async def button_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.next()


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
            init_node = interview.root

            windows = []
            for node in iter_graph(init_node):
                match node:
                    case InitNode(id=node.id):
                        window = Window(
                            Const(node.text),
                            Button(Const("Next"), id="button_init", on_click=button_clicked),
                            state=getattr(states_group, f"state_{node.id}")
                        )
                    case EndNode(id=node.id):
                        window = Window(
                            Const(node.text),
                            Button(Const("Next"), id="button_end", on_click=button_end_clicked),
                            state=getattr(states_group, f"state_{node.id}")
                        )
                    case ChoseQuestionNode(id=node.id):
                        node_id = node.id
                        window = Window(
                            Const(node.text),
                            Select(
                                Format("{item}"),
                                items=node.answers,
                                id="button_select",
                                item_id_getter=lambda ans: f"{node_id}::{ans}",
                                on_click=button_select_clicked,
                            ),
                            state=getattr(states_group, f"state_{node.id}")
                        )
                    case QuestionNode(id=node.id):
                        field = node.tags["field"]
                        window = Window(
                            Const(node.text),
                            TextInput(on_success=next_or_end, id=field),
                            state=getattr(states_group, f"state_{node.id}")
                        )
                    case _:
                        raise ValueError()

                windows.append(window)
            self._items += [
                DialogFactoryItem(
                    interview.name,
                    interview.root,
                    states_group,
                    Dialog(*windows)
                )]

    @staticmethod
    def generate_state(interview) -> type[StatesGroup]:
        return StatesGroupBuilder.build_from(*[node.id for node in iter_graph(interview.root)])


if __name__ == "__main__":
    factory = DialogFactory("/home/dcdnc/mycod/python/path_in_IT_bot/models/interviews")
    for item in factory.items:
        print(item)
