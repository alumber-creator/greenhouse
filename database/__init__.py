from .bot_db import UserDatabase
from .sensor_db import SensorDatabase
from .repositories.user_checks import UserChecksRepository


class Database:
    def __init__(self, sensors):
        self.users = UserDatabase()
        self.sensors = SensorDatabase(sensors)
        self.user_checks = UserChecksRepository

    async def initialize(self):
        await self.users.initialize()
        await self.sensors.initialize()
