from typing import Type, TypeAlias

from aiogram.fsm.state import StatesGroup
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from path_in_IT_bot.builders.abstract_builder import AbstractBuilder
from path_in_IT_bot.entities.producer import Producer
from path_in_IT_bot.models import TelegramBotConsumer

TelegramEntity: TypeAlias = Producer | TelegramBotConsumer


class DialogsBuilder(AbstractBuilder):
    def __init__(self, entity: TelegramEntity, group: Type[StatesGroup]):
        self._entity = entity
        self._group = group
        self._product: Dialog | None = None

    @staticmethod
    def build_from(entity: TelegramEntity, group: Type[StatesGroup]) -> Dialog:
        builder: DialogsBuilder = DialogsBuilder(entity, group)
        builder.produce()

        return builder.product  # type: ignore

    @property
    def product(self) -> Dialog | None:
        return self._product

    def produce(self) -> None:
        if isinstance(self._entity, Producer):
            dialog: Dialog = self.build_producer_dialog()
        elif isinstance(self._entity, TelegramBotConsumer):
            raise NotImplementedError

        self._product = dialog

    def build_producer_dialog(self) -> Dialog:
        if not isinstance(self._entity, Producer):
            raise ValueError

        producer: Producer = self._entity
        message: str = producer.wellcome_message
        buttons = []
        for item in producer.products.keys():
            button = Button(Const(item), id="nothing")
            buttons.append(button)

        return Dialog(Window(
            message, *buttons, state=getattr(self._group, producer.name)
        ))
