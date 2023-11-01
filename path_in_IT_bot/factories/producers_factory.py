from path_in_IT_bot.readers.model_reader import (
    model, TelegramBotProducer, TelegramBotProduct
)

from path_in_IT_bot.factories.abstract_factory import AbstractFactory


class ProducersFactory(AbstractFactory):
    def __init__(self):
        self._items = []

    @property
    def items(self):
        if len(self._items) != len(model.producers):
            self._items.clear()
            for producer_name, producer_model in model.producers:
                self._items.append(Producer(producer_name, producer_model))
        return self._items


class Producer:
    def __init__(self, name: str, producer_model: TelegramBotProducer):
        self._name = name
        self._model = producer_model

    @property
    def name(self):
        return self._name

    @property
    def currency(self) -> str:
        return self._model.currency

    @property
    def wellcome_message(self):
        return self._model.wellcome_message

    @property
    def translate(self):
        return self._model.translate

    @property
    def products(self) -> dict[str, TelegramBotProduct]:
        return self._model.products
