from typing import TypeAlias

from pydantic import BaseModel
from pydantic import PositiveInt

Name: TypeAlias = str


class TelegramBotProduct(BaseModel):
    cost: PositiveInt
    level: PositiveInt


class TelegramBotProducer(BaseModel):
    translate: str
    wellcome_message: str
    currency: str
    products: dict[Name, TelegramBotProduct]


class TelegramBotConsumer(BaseModel):
    pass


class TelegramBotModel(BaseModel):
    bases: dict[str, list[str]]
    producers: dict[Name, TelegramBotProducer]
