import os

import asyncpg  # type: ignore
from dotenv import load_dotenv

load_dotenv()

db_user: str | None = os.getenv("DB_USER")
db_name: str | None = os.getenv("DB_NAME")
db_user_password: str | None = os.getenv("DB_USER_PASSWORD")
db_host: str | None = os.getenv("DB_HOST")


class Database:
    @staticmethod
    async def create_db():
        self = Database()
        self.db_user = db_user
        self.db_name = db_name
        self.db_user_password = db_user_password
        self.db_host = db_host

        conn = await asyncpg.connect(
            user=db_user,
            password=db_user_password,
            database=db_name,
            host=db_host,
        )

        await conn.execute('''
             CREATE TABLE IF NOT EXISTS users (
                tg_id integer PRIMARY KEY 
             );
        ''')

        await conn.close()

        return self
