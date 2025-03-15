import random
from datetime import datetime

from config import Config
from tools.database import Database


class DataGen:
    @staticmethod
    def generate_random_datetimes(start_date: datetime, end_date: datetime, count: int = 1) -> list[datetime]:
        """Генерирует массив случайных дат в указанном временном диапазоне"""
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        start_ts = start_date.timestamp()
        end_ts = end_date.timestamp()

        results = []
        for _ in range(count):
            random_ts = random.uniform(start_ts, end_ts)
            random_date = datetime.fromtimestamp(random_ts)
            results.append(random_date)
        results.sort()

        return results

    @staticmethod
    async def test_generation() -> None:
        """Основная функция генерации тестовых данных"""
        await Database.init_db('sensors.db')
        start_date = datetime(2025, datetime.now().month, 1)
        end_date = datetime(2025, datetime.now().month, 31)
        for sensor in Config.SENSORS:
            for time in DataGen.generate_random_datetimes(start_date, end_date, 1000):
                await Database.insert_sensors(sensor, random.randint(10, 100), time.timestamp())
