from typing import Callable

from databases import Database

database = Database("postgresql+asyncpg://localhost/example")


async def connected(func: Callable) -> Callable:
    async def wrapper(*args, **kwargs) -> None:
        await database.connect()
        func(*args, **kwargs)
        await database.disconnect()

    return wrapper


class DB:
    @connected
    async def create(self):
        ...
