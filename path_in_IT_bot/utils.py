import json
import random
from string import Template, ascii_lowercase
from typing import Iterable, Iterator

# import aiocache
import aiofiles
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from aiocache import Cache
# from redis.asyncio.client import Redis
# from aiocache.serializers import StringSerializer
from aiogram.utils.keyboard import InlineKeyboardBuilder

from path_in_IT_bot.entities.graph import AbstractNode


# @aiocache.cached(
#     ttl=20,
#     serializer=StringSerializer(),
#     cache=Cache.MEMORY,
# )

def find_node(to_find_node_id: str, root):
    for node in iter_graph(root):
        if node.id == to_find_node_id:
            return node


def iter_graph(
        root: AbstractNode,
        _first=True,
        _used: set[AbstractNode] | None = None,
) -> Iterator[AbstractNode]:
    if _used is None:
        _used = set()
    if _first:
        yield root
        _used.add(root)

    for branch in root.branches:
        if branch.to_node in _used:
            continue
        yield branch.to_node
        _used.add(branch.to_node)

    for branch in root.branches:
        yield from iter_graph(branch.to_node, _first=False, _used=_used)


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
