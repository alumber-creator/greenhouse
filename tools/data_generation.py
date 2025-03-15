import random
from datetime import datetime

from configs.config import Config
from database import Database
from database.models import SensorData


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
    async def test_generation(db: Database) -> None:
        """Основная функция генерации тестовых данных"""
        await db.initialize()
        start_date = datetime(datetime.now().year, datetime.now().month, 1)
        end_date = datetime(datetime.now().year, datetime.now().month, 31)
        for sensor in Config.SENSORS:
            for time in DataGen.generate_random_datetimes(start_date, end_date, 1000):
                data = SensorData(
                    sensor_id=sensor,
                    value=random.randint(10, 100),
                    timestamp=time
                )
                await db.sensors.insert_data()
