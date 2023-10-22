from _typeshed import Incomplete
from typing import Callable

database: Incomplete

async def connected(func: Callable) -> Callable: ...

class DB:
    async def create(self) -> None: ...
