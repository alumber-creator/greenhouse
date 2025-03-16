from configs.config import Config
from .bot_db import UserDatabase
from .sensor_db import SensorDatabase
from .repositories.user_checks import UserChecksRepository

class Database:
    def __init__(self):
        self.users = UserDatabase()
        self.sensors = SensorDatabase(Config.SENSORS)
        self.user_checks = UserChecksRepository

    async def initialize(self):
        await self.users.initialize()
        await self.sensors.initialize()