import io
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from matplotlib.dates import DateFormatter, AutoDateLocator


class PlotService:
    @staticmethod
    def generate_plot(sensor_name: str, data: list, period_type: str) -> bytes:
        times = [datetime.fromtimestamp(d[1]) for d in data]
        values = [d[0] for d in data]

        plt.figure(figsize=(12, 6))
        plt.plot(times, values, marker='o' if period_type == 'daily' else None)

        avg = np.mean(values)
        plt.axhline(avg, color='r', linestyle='--', label=f'Avg: {avg:.2f}')
        plt.grid(True)
        plt.legend()

        if period_type == 'daily':
            plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))
            plt.title(f"{sensor_name} - {times[0].strftime('%d.%m.%Y')}")
        else:
            plt.gca().xaxis.set_major_formatter(DateFormatter('%d.%m'))
            plt.gca().xaxis.set_major_locator(AutoDateLocator())
            plt.title(f"{sensor_name} ({times[0].date()} - {times[-1].date()})")

        plt.xticks(rotation=45)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        plt.close()
        return buf.getvalue()
