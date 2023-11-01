from aiogram_dialog import Dialog as Dialog, Window as Window
from aiogram_dialog.widgets.kbd import Button as Button
from aiogram_dialog.widgets.text import Const as Const, Format as Format
from path_in_IT_bot.entities import Entity as Entity
from path_in_IT_bot.factories.abstract_factory import AbstractFactory as AbstractFactory
from path_in_IT_bot.factories.producers_factory import ProducersFactory as ProducersFactory

class DialogsFactory(AbstractFactory):
    def __init__(self, entity_type: Entity) -> None: ...
