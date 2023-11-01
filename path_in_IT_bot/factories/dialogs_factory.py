from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const

from path_in_IT_bot.entities import Entity
from path_in_IT_bot.factories.abstract_factory import AbstractFactory
from path_in_IT_bot.factories.producers_factory import ProducersFactory


class DialogsFactory(AbstractFactory):
    def __init__(self, entity_type: Entity):
        self._entity_type = entity_type
        if entity_type == Entity.PRODUCER:
            self._sub_factory = ProducersFactory()
            self._entities = self._sub_factory.items
        elif entity_type == Entity.CONSUMER:
            raise NotImplemented

    def _window(self):
        ...
