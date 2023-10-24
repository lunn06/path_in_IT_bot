from __future__ import annotations

import os
import asyncpg  # type: ignore
from dotenv import load_dotenv

load_dotenv()

_db_user: str | None = os.getenv("DB_USER")
_db_name: str | None = os.getenv("DB_NAME")
_db_user_password: str | None = os.getenv("DB_USER_PASSWORD")
_db_host: str | None = os.getenv("DB_HOST")


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
                tg_id integer PRIMARY KEY 
             );
        ''')

        await conn.close()

    @staticmethod
    async def create() -> Database:
        if (_db_user is None) or (_db_name is None) or (_db_user_password is None) or (_db_host is None):
            raise ValueError("DatabaseCreationError: Bad config")

        db = Database(_db_user, _db_name, _db_user_password, _db_host)

        conn = await asyncpg.connect(
            user=db.db_user,
            password=db.db_user_password,
            database=db.db_name,
            host=db.db_host,
        )

        await conn.execute('''
             CREATE TABLE IF NOT EXISTS users (
                tg_id integer PRIMARY KEY 
             );
        ''')

        await conn.close()

        return db


class Connection:

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


def connect_to(db: Database) -> Connection:
    return Connection(db)
