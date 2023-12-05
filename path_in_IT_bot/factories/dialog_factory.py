from aiogram.fsm.state import StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.text import Const, Format

from path_in_IT_bot.builders.states_builder import StatesGroupBuilder
from path_in_IT_bot.entities.graph import AbstractNode, InitNode, EndNode, ChoseQuestionNode, QuestionNode
from path_in_IT_bot.entities.interveiw import Interview
from path_in_IT_bot.factories.abstract_factory import AbstractFactory
from path_in_IT_bot.factories.interviews_factory import InterviewsFactory
from path_in_IT_bot.utils import iter_graph, validated, find_node


async def button_end_clicked(_callback: CallbackQuery, _buttton: Button, manager: DialogManager):
    await manager.done()


async def button_select_clicked(
        _callback: CallbackQuery,
        _select: Select,
        manager: DialogManager,
        item_id: str
):
    ans = item_id

    factory_item: DialogFactoryItem = validated(manager).start_data

    state_group, state_name = validated(manager).current_context().state.state.split(":")
    cur_node_id = state_name.removeprefix("state_")
    cur_node = find_node(cur_node_id, factory_item.root)

    manager.dialog_data[cur_node.tags["field"]] = ans

    for branch in cur_node.branches:
        if branch.label == ans:
            await manager.switch_to(getattr(factory_item.states, f"state_{branch.to_node.id}"))


async def name_handler(_message: Message, _widget, manager: DialogManager, *_):
    factory_item: DialogFactoryItem = validated(manager.start_data)
    state_group, state_name = validated(manager).current_context().state.state.split(":")
    cur_node_id = state_name.removeprefix("state_")

    cur_node = find_node(cur_node_id, factory_item.root)

    field = cur_node.tags["field"]
    name = validated(manager).find(field).get_value()
    manager.dialog_data[field] = name

    await manager.next()


async def button_clicked(_callback: CallbackQuery, _button: Button, manager: DialogManager):
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
                    case InitNode(id=node.id) as init_node:
                        window = DialogFactory.process_init_window(init_node, states_group)
                    case EndNode(id=node.id) as end_node:
                        window = DialogFactory.process_end_window(end_node, states_group)
                    case ChoseQuestionNode(id=node.id) as choose_node:
                        window = DialogFactory.process_choose_window(choose_node, states_group)
                    case QuestionNode(id=node.id) as question_node:
                        window = DialogFactory.process_question_window(question_node, states_group)
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

    @staticmethod
    def process_init_window(node: InitNode, states_group: type[StatesGroup]) -> Window:
        window = Window(
            Const(node.text),
            Button(Const("Next"), id="button_init", on_click=button_clicked),
            state=getattr(states_group, f"state_{node.id}")
        )
        return window

    @staticmethod
    def process_end_window(node: EndNode, states_group: type[StatesGroup]) -> Window:
        window = Window(
            Const(node.text),
            Button(Const("Next"), id="button_end", on_click=button_end_clicked),
            state=getattr(states_group, f"state_{node.id}")
        )

        return window

    @staticmethod
    def process_choose_window(node: ChoseQuestionNode, states_group: type[StatesGroup]) -> Window:
        window = Window(
            Const(node.text),
            Select(
                Format("{item}"),
                items=node.answers,
                id="button_select",
                item_id_getter=lambda ans: ans,
                on_click=button_select_clicked,  # type: ignore
            ),
            state=getattr(states_group, f"state_{node.id}")
        )

        return window

    @staticmethod
    def process_question_window(node: QuestionNode, states_group: type[StatesGroup]) -> Window:
        field = node.tags["field"]
        window = Window(
            Const(node.text),
            TextInput(on_success=name_handler, id=field),  # type: ignore
            state=getattr(states_group, f"state_{node.id}")
        )

        return window


if __name__ == "__main__":
    factory = DialogFactory("/home/dcdnc/mycod/python/path_in_IT_bot/models/interviews")
    for item in factory.items:
        print(item)
