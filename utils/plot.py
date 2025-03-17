import asyncio
import datetime

import matplotlib.pyplot as plt
from io import BytesIO
from config import db


class PlotGenerator:
    @staticmethod
    async def generate_plot(sensor_id: str, date: datetime) -> BytesIO | None:
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start.replace(day=date.day + 1)

        data = await db.sensors.get_data(
            f"SELECT * FROM {sensor_id} WHERE time BETWEEN ? AND ?",
            (start, end)
        )
        if not data:
            return None

        def sync_plot():
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

        return await asyncio.to_thread(sync_plot)
