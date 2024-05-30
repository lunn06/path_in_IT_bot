from __future__ import annotations

from typing import Any

import asyncpg  # type: ignore
from asyncpg import Record

from path_in_IT_bot.readers.config_reader import config


class DBUser:
    def __init__(self, db_user: str, db_name: str, db_user_password: str, db_host: str) -> None:
        self._db_user = db_user
        self._db_name = db_name
        self._db_user_password = db_user_password
        self._db_host = db_host

    async def initiate(self) -> None:
        conn = await asyncpg.connect(
            user=self._db_user,
            password=self._db_user_password,
            database=self._db_name,
            host=self._db_host,
        )

        await conn.execute('''
             CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                currency INTEGER,
                currency_descripted BOOL
             );
        ''')

        await conn.close()

    async def _execute_with(self, conn: DatabaseConnection | None, execute_command: str, *args: Any) -> None:
        if isinstance(conn, DatabaseConnection):
            await conn.cursor.execute(execute_command, *args)
        else:
            async with connect(self) as cursor:
                await cursor.execute(execute_command, *args)

    async def _fetch_with(self, conn: DatabaseConnection | None, fetch_command: str, *args: Any) -> list[Record]:
        if isinstance(conn, DatabaseConnection):
            return await conn.cursor.fetch(fetch_command, *args)
        else:
            async with connect(self) as cursor:
                return await cursor.fetch(fetch_command, *args)

    async def is_currency_descripted(self, tg_id: int, conn: DatabaseConnection | None = None) -> bool:
        fetch_command = "SELECT currency_descripted FROM users WHERE tg_id = $1 LIMIT 1"

        return (await self._fetch_with(conn, fetch_command, tg_id))[0]["currency_descripted"]

    async def set_currency_descripted(
            self,
            tg_id: int,
            new_currency_descripted: bool,
            conn: DatabaseConnection | None = None
    ) -> None:
        update_command = "UPDATE users SET currency_descripted = $1 WHERE tg_id = $2"

        await self._execute_with(conn, update_command, new_currency_descripted, tg_id)

    async def add(self, tg_id: int, conn: DatabaseConnection | None = None) -> None:
        execute_command = '''INSERT INTO users(
                tg_id, 
                currency, 
                currency_descripted
            ) VALUES($1, $2, $3) ON CONFLICT(tg_id) DO NOTHING'''

        await self._execute_with(conn, execute_command, tg_id, config.initial_currency, False)

    async def get(self, tg_id, conn: DatabaseConnection | None = None) -> list[Record]:
        fetch_command = "SELECT * FROM users WHERE tg_id = $1 LIMIT 1"

        return await self._fetch_with(conn, fetch_command, tg_id)

    async def get_currency(self, tg_id, conn: DatabaseConnection | None = None) -> int:
        fetch_command = "SELECT currency FROM users WHERE tg_id = $1 LIMIT 1"

        return (await self._fetch_with(conn, fetch_command, tg_id))[0]["currency"]

    async def get_all(self, conn: DatabaseConnection | None = None) -> list[Record]:
        fetch_command = "SELECT * FROM users"

        return await self._fetch_with(conn, fetch_command)

    @staticmethod
    async def create() -> DBUser:
        db = DBUser(
            config.db_user,
            config.db_name,
            config.db_user_password.get_secret_value(),
            str(config.db_host),
        )

        await db.initiate()

        return db


class DatabaseConnection:

    def __init__(self, db: DBUser):
        self.db = db

    async def __aenter__(self):
        self.cursor = await asyncpg.connect(
            user=self.db._db_user,
            password=self.db._db_user_password,
            database=self.db._db_name,
            host=self.db._db_host,
        )

        return self.cursor

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cursor.close()


def connect(db: DBUser) -> DatabaseConnection:
    return DatabaseConnection(db)
