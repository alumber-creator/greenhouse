from typing import Iterable, Any

from .base import DatabaseHandler
from .models import SensorData
import aiosqlite as sql
import logging


class SensorDatabase(DatabaseHandler):
    """Класс для работы с данными сенсоров"""

    def __init__(self, sensors):
        super().__init__("sensors.db")
        self._allowed_sensors = sensors
        self._init = False

    async def initialize(self):
        """Инициализация таблиц для сенсоров"""
        async with self.connection() as conn:
            for sensor in self._allowed_sensors:
                if not self._validate_sensor_name(sensor):
                    raise ValueError(f"Invalid sensor name: {sensor}")

                await conn.execute(f'''
                    CREATE TABLE IF NOT EXISTS "{sensor}" (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        value FLOAT,
                        time DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
            await conn.commit()
        self._init = True
        logging.info("Sensor database initialized")

    def _validate_sensor_name(self, name: str) -> bool:
        """Валидация имени сенсора"""
        return name.isidentifier() and name in self._allowed_sensors

    async def insert_data(self, sensor, data: SensorData) -> bool:
        """Вставка данных сенсора"""
        if not self._validate_sensor_name(sensor):
            raise ValueError(f"Invalid sensor ID: {sensor}")

        try:
            await self.execute(
                f'INSERT INTO "{sensor}" (value, time) VALUES (?, ?)',
                (data.value, data.timestamp)
            )
            return True
        except sql.Error as e:
            logging.error(f"Failed to insert sensor data: {str(e)}")
            return False

    async def get_data(self, query: str, params: Iterable[Any] = ()) -> list[SensorData]:
        """Получение всех результатов запроса"""
        results = await self.fetch_all(query, params)
        return [SensorData.model_validate({
                "value": float(row[1]),
                "timestamp": (row[2]),
            }) for row in results]


