import asyncio
import datetime

import matplotlib.pyplot as plt
from io import BytesIO
from config import db


class PlotGenerator:
    @staticmethod
    async def generate_plot(sensor_id: str, start_date: datetime, end_date: datetime) -> BytesIO | None:
        query = f"SELECT * FROM {sensor_id} WHERE time BETWEEN ? AND ?"
        params = (start_date, end_date)
        data = await db.sensors.get_data(query, params)
        if not data:
            return None

        fig, ax = plt.subplots(figsize=(12, 6))
        timestamps = [d.timestamp for d in data]
        timestamps.sort()
        values = [d.value for d in data]

        ax.plot(timestamps, values)
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.set_title(f'Sensor {sensor_id}')
        fig.autofmt_xdate()

        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf
