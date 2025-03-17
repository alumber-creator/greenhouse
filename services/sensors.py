from datetime import datetime

from pydantic import TypeAdapter

from database import Database
from database.models import SensorData


class SensorService:
    def __init__(self):
        self.db = Database().sensors

    async def get_sensor_data(
            self,
            sensor_name: str,
            start_date: datetime,
            end_date: datetime
    ) -> list[SensorData]:
        """Получение данных сенсора за период"""
        start_ts = start_date.timestamp()
        end_ts = end_date.timestamp()

        query = f"""
            SELECT value, time FROM "{sensor_name}"
            WHERE time BETWEEN ? AND ?
            ORDER BY time
        """

        results = await self.db.fetch_all(query, (start_ts, end_ts))
        return TypeAdapter(list[SensorData]).validate_python([
            {'sensor_id': sensor_name, 'value': row[0], 'timestamp': row[1]}
            for row in results
        ])
