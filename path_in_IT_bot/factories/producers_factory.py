from path_in_IT_bot.entities.producer import Producer
from path_in_IT_bot.readers.model_reader import model
from path_in_IT_bot.entities.producer import Producer

from path_in_IT_bot.factories.abstract_factory import AbstractFactory


class ProducersFactory(AbstractFactory):
    def __init__(self):
        self._items = []

    @property
    def items(self):
        if len(self._items) != len(model.producers):
            self._items.clear()
            for producer_name, producer_model in model.producers.items():
                self._items.append(Producer(producer_name, producer_model))
        return self._items
