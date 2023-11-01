from path_in_IT_bot.models import TelegramBotProducer, TelegramBotProduct


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
