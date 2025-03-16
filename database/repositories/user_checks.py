from contextlib import asynccontextmanager
from database.bot_db import UserDatabase
from typing import Tuple


class UserChecksRepository:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.db = UserDatabase()

    @asynccontextmanager
    async def _get_connection(self):
        async with self.db.connection() as conn:
            yield conn

    async def get_or_create_checks(self) -> Tuple[int, int, int]:
        """Получение или создание настроек пользователя"""
        async with self._get_connection() as conn:
            cursor = await conn.execute(
                "SELECT check1, check2, check3 FROM user_checks WHERE user_id = ?",
                (self.user_id,)
            )
            result = await cursor.fetchone()

            if not result:
                await conn.execute(
                    "INSERT INTO user_checks (user_id) VALUES (?)",
                    (self.user_id,)
                )
                return (0, 0, 0)
            return result

    async def toggle_check(self, check_name: str) -> Tuple[int, int, int]:
        """Переключение состояния конкретной настройки"""
        allowed_columns = {"check1", "check2", "check3"}
        if check_name not in allowed_columns:
            raise ValueError("Invalid check name")

        async with self._get_connection() as conn:
            await conn.execute(
                f"UPDATE user_checks SET {check_name} = NOT {check_name} WHERE user_id = ?",
                (self.user_id,)
            )
            cursor = await conn.execute(
                "SELECT check1, check2, check3 FROM user_checks WHERE user_id = ?",
                (self.user_id,)
            )
            return await cursor.fetchone()