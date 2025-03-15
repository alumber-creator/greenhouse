import aiosqlite as sql
from contextlib import asynccontextmanager
from collections.abc import Iterable, AsyncIterator
from typing import Any


class DatabaseHandler:
    """Класс с корректным управлением подключениями"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[sql.Connection]:
        """Корректный асинхронный контекстный менеджер"""
        conn = await sql.connect(self.db_path)
        try:
            yield conn
        finally:
            await conn.close()

    async def execute(self, query: str, params: Iterable[Any] = ()) -> None:
        """Выполнение запроса с автоматическим управлением подключением"""
        async with self.connection() as conn:
            await conn.execute(query, params)
            await conn.commit()

    async def fetch_all(self, query: str, params: Iterable[Any] = ()) -> list[tuple]:
        """Получение всех результатов запроса"""
        async with self.connection() as conn:
            cursor = await conn.execute(query, params)
            return await cursor.fetchall()