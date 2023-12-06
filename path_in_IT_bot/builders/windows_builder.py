from typing import override, Callable, Awaitable, TypeAlias, Any

from aiogram.fsm.state import StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd.select import OnItemClick
from aiogram_dialog.widgets.input.text import OnSuccess, TextInput

from path_in_IT_bot.utils import validated, find_node
from path_in_IT_bot.builders.abstract_builder import AbstractBuilder
from path_in_IT_bot.entities.graph import AbstractNode, InitNode, EndNode, ChooseQuestionNode, QuestionNode


async def button_end_clicked(_callback: CallbackQuery, _buttton: Button, manager: DialogManager):
    await manager.done()


async def button_select_clicked(
        _callback: CallbackQuery,
        _select: Select,
        manager: DialogManager,
        item_id: str
):
    ans = item_id

    factory_item = validated(manager).start_data

    state_group, state_name = validated(manager).current_context().state.state.split(":")
    cur_node_id = state_name.removeprefix("state_")
    cur_node = find_node(cur_node_id, factory_item.root)

    manager.dialog_data[cur_node.tags["field"]] = ans

    for branch in cur_node.branches:
        if branch.label == ans:
            await manager.switch_to(getattr(factory_item.states, f"state_{branch.to_node.id}"))


async def text_handler(_message: Message, _widget, manager: DialogManager, *_):
    factory_item = validated(manager.start_data)
    state_group, state_name = validated(manager).current_context().state.state.split(":")
    cur_node_id = state_name.removeprefix("state_")

    cur_node = find_node(cur_node_id, factory_item.root)

    field = cur_node.tags["field"]
    name = validated(manager).find(field).get_value()
    manager.dialog_data[field] = name

    await manager.next()


async def button_clicked(_callback: CallbackQuery, _button: Button, manager: DialogManager):
    await manager.next()


OnClick: TypeAlias = Callable[[CallbackQuery, "Button", DialogManager], Awaitable]


class WindowBuilder(AbstractBuilder):
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

    @override
    @property
    def product(self) -> Window:
        return self._product

    @override
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
                    choose_node, self._states_group, button_select_clicked  # type: ignore
                )
            case QuestionNode(id=self._node.id) as question_node:
                window = WindowBuilder.process_question_window(
                    question_node, self._states_group, text_handler  # type: ignore
                )
            case _:
                raise ValueError()
        self._product = window

    @staticmethod
    @override
    def build_from(
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
        field = node.tags["field"]
        window = Window(
            Const(node.text),
            TextInput(on_success=on_success, id=field),
            state=getattr(states_group, f"state_{node.id}")
        )

        return window
