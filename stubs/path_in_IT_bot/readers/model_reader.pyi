from _typeshed import Incomplete
from pydantic import BaseModel, PositiveInt as PositiveInt
from typing import TypeAlias

Name: TypeAlias

class TelegramBotProduct(BaseModel):
    cost: PositiveInt
    level: PositiveInt

class TelegramBotProducer(BaseModel):
    translate: str
    wellcome_message: str
    currency: str
    products: dict[Name, TelegramBotProduct]

class TelegramBotModel(BaseModel):
    bases: dict[str, list[str]]
    producers: dict[Name, TelegramBotProducer]

model: Incomplete
