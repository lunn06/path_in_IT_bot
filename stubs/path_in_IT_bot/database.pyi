from _typeshed import Incomplete
from path_in_IT_bot.readers.config_reader import config as config

class Database:
    db_user: Incomplete
    db_name: Incomplete
    db_user_password: Incomplete
    db_host: Incomplete
    def __init__(self, db_user: str, db_name: str, db_user_password: str, db_host: str) -> None: ...
    async def initiate(self) -> None: ...
    async def add_new_user(self, tg_id: int): ...
    async def get_all_users(self): ...
    @staticmethod
    async def create() -> Database: ...

class DatabaseConnection:
    db: Incomplete
    def __init__(self, db: Database) -> None: ...
    conn: Incomplete
    async def __aenter__(self): ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...

def connect(db: Database) -> DatabaseConnection: ...
