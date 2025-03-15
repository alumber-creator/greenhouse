import logging
from collections.abc import Iterable
from typing import Any, Optional
import aiosqlite as sql
from config import Config


class Database:
    BOT_DB = "bot.db"
    SENSOR_DB = "sensors.db"

    @staticmethod
    async def _execute(base: str, query: str, params: Iterable[Any] = ()) -> None:
        """Безопасное выполнение запроса с параметрами"""
        async with sql.connect(base) as db:
            await db.execute(query, params)
            await db.commit()

    @staticmethod
    async def init_db(name: str = SENSOR_DB) -> None:
        """Инициализация БД с валидацией имён таблиц"""
        allowed_tables = Config.SENSORS if name == Database.SENSOR_DB else []

        if name == Database.SENSOR_DB:
            for sensor in allowed_tables:
                if not sensor.isidentifier():  # Проверка на корректное имя таблицы
                    raise ValueError(f"Invalid table name: {sensor}")

                await Database._execute(name, f'''
                    CREATE TABLE IF NOT EXISTS "{sensor}" (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        value FLOAT,
                        time DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')

        elif name == Database.BOT_DB:
            await Database._execute(name, """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL UNIQUE,
                    username TEXT,
                    role TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )""")

            await Database._execute(name, '''
                CREATE TABLE IF NOT EXISTS user_checks (
                    user_id INTEGER PRIMARY KEY,
                    check1 INTEGER DEFAULT 0,
                    check2 INTEGER DEFAULT 0,
                    check3 INTEGER DEFAULT 0
                )''')

        logging.info(f"База данных {name} инициализирована")


    @staticmethod
    async def add_user(user_data: dict) -> None:
        """Добавление пользователя с параметризацией"""
        query = """
            INSERT INTO users (user_id, username) 
            VALUES (?, ?)
        """
        try:
            await Database._execute(
                Database.BOT_DB,
                query,
                (user_data['user_id'], user_data['username'])
            )
            logging.info("Пользователь добавлен")
        except sql.IntegrityError:
            logging.warning("Пользователь уже существует!")


    @staticmethod
    async def insert_sensors(sensor: str, value: float, time: float) -> None:
        """Вставка данных сенсора с проверкой имени таблицы"""
        if sensor not in Config.SENSORS:
            raise ValueError(f"Invalid sensor: {sensor}")

        query = f'''
            INSERT INTO "{sensor}" (value, time) 
            VALUES (?, ?)
        '''
        await Database._execute(Database.SENSOR_DB, query, (value, time))


    @staticmethod
    async def get_users(
            conditions: str,
            params: Optional[Iterable] = None
    ) -> list[tuple]:
        async with sql.connect(Database.BOT_DB) as db:
            query = f"SELECT * FROM users WHERE {conditions}"
            async with db.execute(query, params or ()) as cursor:
                return await cursor.fetchall()

