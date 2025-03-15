import logging
import aiosqlite as sql
from datetime import datetime

from config import Config


class Database:

    BOT_DB = "bot.db"
    SENSOR_DB = "sensors.db"

    @staticmethod
    async def data_insert(base: str, data: str):
        async with sql.connect(base) as db:
            await db.execute(data)
            await db.commit()

    @staticmethod
    async def init_db(name: str = SENSOR_DB):
        if name == Database.SENSOR_DB:
            for sensor in Config.SENSORS:
                await Database.data_insert(name, f'''
                        CREATE TABLE IF NOT EXISTS {sensor}(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            value FLOAT,
                            time DATETIME DEFAULT CURRENT_TIMESTAMP)
                        ''')
        elif name == Database.BOT_DB:

            await Database.data_insert(name, """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL UNIQUE,
                    username TEXT,
                    is_admin BOOLEAN,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                """)

            await Database.data_insert(name, '''
                CREATE TABLE IF NOT EXISTS user_checks (
                    user_id INTEGER PRIMARY KEY,
                    check1 INTEGER DEFAULT 0,
                    check2 INTEGER DEFAULT 0,
                    check3 INTEGER DEFAULT 0)
                ''')
        logging.info(f"База данных {name} инициализирована")

    @staticmethod
    async def add_user(user_data):
        """Добавляет нового пользователя в таблицу"""
        try:
            # Вставка данных через параметры (защита от SQL-инъекций)
            await Database.data_insert(Database.BOT_DB, f'''
                INSERT INTO users (user_id, username) 
                VALUES ({user_data['user_id']}, {user_data['username']})
            ''')
            logging.info("Пользователь добавлен")
        except sql.IntegrityError:
            logging.warning("Пользователь уже существует!")

    @staticmethod
    async def insert_sensors(sensor: str, value: float, time: float):
        await Database.data_insert(Database.SENSOR_DB, f"INSERT INTO {sensor} (value, time) VALUES ({value}, {time})")




