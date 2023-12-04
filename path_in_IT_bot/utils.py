import json
import random
from typing import Iterable, Generator
from string import Template, ascii_lowercase

# import aiocache
import aiofiles
# from aiocache import Cache
# from redis.asyncio.client import Redis
# from aiocache.serializers import StringSerializer
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from path_in_IT_bot.entities.graph import AbstractNode


# @aiocache.cached(
#     ttl=20,
#     serializer=StringSerializer(),
#     cache=Cache.MEMORY,
# )

def iter_over_graph(root: AbstractNode, _first=True) -> Generator[AbstractNode, None, None]:
    if _first:
        yield root

    for branch in root.branches:
        yield branch.to_node

    for branch in root.branches:
        yield from iter_over_graph(branch.to_node, False)


def random_str(length: int) -> str:
    return ''.join(random.choice(ascii_lowercase) for _ in range(length))


def validated[T](value: T) -> T:
    if value is None:
        raise RuntimeError("Invalid value")
    return value


async def get_text(text_key: str, **kwargs: str) -> str:
    async with aiofiles.open("models/text.json", 'r') as file:
        messages = json.loads(await file.read())

    text = messages.get(text_key, "Something went wrong")
    return Template(text).substitute(kwargs)


async def build_inline_start_kb(callback_data: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    inline_text = await get_text("start_inline_text")
    builder.add(InlineKeyboardButton(
        text=inline_text,
        callback_data=callback_data
    ))

    return builder.as_markup()


def build_kb(items: Iterable[str]) -> list[list[KeyboardButton]]:
    return [[KeyboardButton(text=item)] for item in items]
