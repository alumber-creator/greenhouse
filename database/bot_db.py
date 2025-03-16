from .base import DatabaseHandler
import logging
import aiosqlite as sql

from .models import User


class UserDatabase(DatabaseHandler):
    def __init__(self):
        super().__init__("bot.db")
        self._initialized = False

    async def initialize(self):
        """Инициализация с проверкой состояния"""
        if self._initialized:
            return

        async with self.connection() as conn:
            # Создаем таблицы в одной транзакции
            await conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL UNIQUE,
                    username TEXT,
                    role TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS user_checks (
                    user_id INTEGER PRIMARY KEY,
                    check1 INTEGER DEFAULT 0,
                    check2 INTEGER DEFAULT 0,
                    check3 INTEGER DEFAULT 0
                );
            """)
            await conn.commit()

        self._initialized = True
        logging.info("User database initialized")

    async def add_user(self, user_data: User) -> bool:
        """Добавление пользователя с обработкой ошибок"""
        try:
            await self.execute(
                "INSERT INTO users (user_id, username, role) VALUES (?, ?, ?)",
                (user_data.user_id, user_data.username, user_data.role)
            )
            return True
        except sql.IntegrityError as e:
            logging.warning(f"User already exists: {e}")
            return False
        except Exception as e:
            logging.error(f"Database error: {e}")
            return False

    async def get_users(self, conditions: str = "1=1", params: tuple = ()) -> list[User]:
        """Получение пользователей с фильтрацией"""
        query = f"SELECT * FROM users WHERE {conditions}"
        results = await self.fetch_all(query, params)
        return [User.parse_obj({
            "user_id": row[1],
            "username": row[2],
            "role": row[3],
            "created_at": row[4]
        }) for row in results]
