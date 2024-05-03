from typing import override

from aiogram.fsm.state import StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input.text import OnSuccess, TextInput
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.kbd.select import OnItemClick
from aiogram_dialog.widgets.text import Const, Format

from path_in_IT_bot.entities.graph import AbstractNode, InitNode, EndNode, ChooseQuestionNode, QuestionNode
from path_in_IT_bot.utils import validated, find_node


async def button_end_clicked(_callback: CallbackQuery, _button: Button, manager: DialogManager, *_):
    await manager.done()


async def button_select_clicked(
        _callback: CallbackQuery,
        _select: Select,
        manager: DialogManager,
        item_id: str,
        *_
):
    ans = item_id

    factory_item = validated(manager).start_data

    state_group, state_name = validated(manager).current_context().state.state.split(":")
    cur_node_id = state_name.removeprefix("state_")
    cur_node: ChooseQuestionNode = find_node(cur_node_id, factory_item.root)

    manager.dialog_data[cur_node.field] = ans

    for branch in cur_node.branches:
        if branch.label == ans:
            await manager.switch_to(getattr(factory_item.states, f"state_{branch.to_node.id}"))


async def text_handler(_message: Message, _text_input: TextInput, manager: DialogManager, *_):
    factory_item = validated(manager.start_data)
    state_group, state_name = validated(manager).current_context().state.state.split(":")
    cur_node_id = state_name.removeprefix("state_")

    cur_node: QuestionNode = find_node(cur_node_id, factory_item.root)

    field = cur_node.field
    name = validated(manager).find(field).get_value()
    manager.dialog_data[field] = name

    await manager.next()


# Usage: InitWindow
async def button_clicked(_callback: CallbackQuery, _button: Button, manager: DialogManager, *_):
    await manager.next()


class InitWindow(Window):
    def __init__(self, node: AbstractNode, states_group: type[StatesGroup], on_click=button_clicked):
        super().__init__(
            Const(node.text),
            Button(Const("Next"), id="button_init", on_click=on_click),
            state=getattr(states_group, f"state_{node.id}")
        )

        self.node = node
        self.states_group = states_group


class EndWindow(Window):
    def __init__(self, node: AbstractNode, states_group: type[StatesGroup], on_click=button_clicked):
        super().__init__(
            Const(node.text),
            Button(Const("Закончить"), id="button_end", on_click=on_click),
            state=getattr(states_group, f"state_{node.id}")
        )

        self.node = node
        self.states_group = states_group

class WindowBuilder:
    _product: Window
    _node: AbstractNode
    _states_group: type[StatesGroup]

    # _on_click: OnClick | None
    # _on_item_click: OnItemClick | None
    # _on_success: OnSuccess | None

    def __init__(
            self,
            node: AbstractNode,
            states_group: type[StatesGroup],
            # on_click: OnClick | None,
            # on_item_click: OnItemClick | None,
            # on_success: OnSuccess | None,
    ) -> None:
        self._node = node
        self._states_group = states_group
        # self._on_click = on_click
        # self._on_item_click = on_item_click
        # self._on_success = on_success

    @property
    def product(self) -> Window:
        return self._product

    def produce(self) -> None:
        match self._node:
            case InitNode(id=self._node.id) as init_node:
                window = WindowBuilder.process_init_window(
                    init_node, self._states_group, button_clicked
                )
            case EndNode(id=self._node.id) as end_node:
                window = WindowBuilder.process_end_window(
                    end_node, self._states_group, button_end_clicked
                )
            case ChooseQuestionNode(id=self._node.id) as choose_node:
                window = WindowBuilder.process_choose_window(
                    choose_node, self._states_group, button_select_clicked
                )
            case QuestionNode(id=self._node.id) as question_node:
                window = WindowBuilder.process_question_window(
                    question_node, self._states_group, text_handler
                )
            case _:
                raise ValueError()
        self._product = window

    @staticmethod
    @override
    def build(
            node: AbstractNode,
            states_group: type[StatesGroup],
            # on_click: OnClick | None,
            # on_item_click: OnItemClick | None,
            # on_success: OnSuccess | None,
    ) -> Window:
        builder = WindowBuilder(
            node,
            states_group,
            # on_click=on_click,
            # on_item_click=on_item_click,
            # on_success=on_success
        )
        builder.produce()

        return builder.product

    @staticmethod
    def process_init_window(node: InitNode, states_group: type[StatesGroup], on_click: OnClick) -> Window:
        window = Window(
            Const(node.text),
            Button(Const("Next"), id="button_init", on_click=on_click),
            state=getattr(states_group, f"state_{node.id}")
        )
        return window

    @staticmethod
    def process_end_window(
            node: EndNode,
            states_group: type[StatesGroup],
            on_click: OnClick
    ) -> Window:
        window = Window(
            Const(node.text),
            Button(Const("Next"), id="button_end", on_click=on_click),
            state=getattr(states_group, f"state_{node.id}")
        )

        return window

    @staticmethod
    def process_choose_window(
            node: ChooseQuestionNode,
            states_group: type[StatesGroup],
            on_click: OnItemClick
    ) -> Window:
        window = Window(
            Const(node.text),
            Select(
                Format("{item}"),
                items=node.answers,
                id="button_select",
                item_id_getter=lambda ans: ans,
                on_click=on_click,
            ),
            state=getattr(states_group, f"state_{node.id}")
        )

        return window

    @staticmethod
    def process_question_window(
            node: QuestionNode,
            states_group: type[StatesGroup],
            on_success: OnSuccess
    ) -> Window:
        window = Window(
            Const(node.text),
            # Cancel(),
            TextInput(on_success=on_success, id=node.field),
            state=getattr(states_group, f"state_{node.id}"),
            # preview_add_transitions=[Next()]
        )

        return window


if __name__ == "__main__":
    print(button_end_clicked.__name__)