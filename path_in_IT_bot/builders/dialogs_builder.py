from typing import Iterable, Type, TypeAlias

from aiogram_dialog import Window, Dialog
from aiogram.fsm.state import StatesGroup
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const

from path_in_IT_bot.models import TelegramBotProducer, TelegramBotConsumer
from path_in_IT_bot.entities.producer import Producer

TelegramEntity: TypeAlias = Producer | TelegramBotConsumer


class DialogsBuilder:
    def __init__(self, entity: TelegramEntity, group: Type[StatesGroup]):
        self._entity = entity
        self._group = group

    @staticmethod
    def build_from(entity: TelegramEntity, group: Type[StatesGroup]) -> Dialog:
        builder = DialogsBuilder(entity, group)
        return builder.build()

    @property
    def entity(self):
        return self._entity

    def build(self) -> Dialog:
        if isinstance(self._entity, Producer):
            dialog: Dialog = self.build_producer_dialog()
        elif isinstance(self._entity, TelegramBotConsumer):
            raise NotImplementedError

        return dialog

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
