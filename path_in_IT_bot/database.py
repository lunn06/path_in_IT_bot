from __future__ import annotations

import asyncpg  # type: ignore

from path_in_IT_bot.readers.config_reader import config


class Database:
    def __init__(self, db_user: str, db_name: str, db_user_password: str, db_host: str):
        self.db_user = db_user
        self.db_name = db_name
        self.db_user_password = db_user_password
        self.db_host = db_host

    async def initiate(self):
        conn = await asyncpg.connect(
            user=self.db_user,
            password=self.db_user_password,
            database=self.db_name,
            host=self.db_host,
        )

        await conn.execute('''
             CREATE TABLE IF NOT EXISTS users (
                tg_id integer PRIMARY KEY,
                score integer
             );
        ''')

        await conn.close()

    async def add_new_user(self, tg_id: int):
        async with connect(self) as conn:
            await conn.execute('''
                INSERT INTO users (tg_id, score) VALUES ($1, $2) ON CONFLICT (tg_id) DO NOTHING
            ''', tg_id, 0)

    async def get_all_users(self):
        async with connect(self) as conn:
            return await conn.fetch('''
                SELECT * FROM USERS 
            ''')

    @staticmethod
    async def create() -> Database:
        db = Database(
            config.db_user,
            config.db_name,
            config.db_user_password.get_secret_value(),
            config.db_host
        )

        await db.initiate()

        return db


class DatabaseConnection:

    def __init__(self, db: Database):
        self.db = db

    async def __aenter__(self):
        self.conn = await asyncpg.connect(
            user=self.db.db_user,
            password=self.db.db_user_password,
            database=self.db.db_name,
            host=self.db.db_host,
        )

        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()


def connect(db: Database) -> DatabaseConnection:
    return DatabaseConnection(db)
