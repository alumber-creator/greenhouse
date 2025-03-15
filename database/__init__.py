from .bot_db import UserDatabase
from .sensor_db import SensorDatabase


class Database:
    def __init__(self, sensors):
        self.users = UserDatabase()
        self.sensors = SensorDatabase(sensors)

    async def initialize(self):
        """Инициализация всех компонентов БД"""
        await self.users.initialize()
        await self.sensors.initialize()
