from _typeshed import Incomplete

db_user: str | None
db_name: str | None
db_user_password: str | None
db_host: str | None

class Database:
    db_user: Incomplete
    db_name: Incomplete
    db_user_password: Incomplete
    db_host: Incomplete
    @staticmethod
    async def create_db(): ...
