# bot/keyboards/graph.py
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
import calendar

from config import Config


class GraphMenu:
    @staticmethod
    async def sensors_menu():
        builder = InlineKeyboardBuilder()
        for sensor in Config.SENSORS:
            builder.button(
                text=f"Sensor {sensor}", 
                callback_data=f"sensor:{sensor}"
            )
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    async def years_menu():
        builder = InlineKeyboardBuilder()
        current_year = datetime.now().year
        for year in range(current_year - 5, current_year + 1):
            builder.button(
                text=str(year), 
                callback_data=f"year:{year}"
            )
        builder.button(text="↩️ Cancel", callback_data="back")
        builder.adjust(3)
        return builder.as_markup()

    @staticmethod
    async def months_menu(year: int):
        builder = InlineKeyboardBuilder()
        for month in range(1, 13):
            builder.button(
                text=datetime(year, month, 1).strftime("%B"),
                callback_data=f"month:{month}"
            )
        builder.button(text="↩️ Back", callback_data="back")
        builder.adjust(3)
        return builder.as_markup()

    @staticmethod
    async def days_menu(year: int, month: int):
        builder = InlineKeyboardBuilder()
        num_days = calendar.monthrange(year, month)[1]
        for day in range(1, num_days + 1):
            builder.button(
                text=str(day), 
                callback_data=f"day:{day}"
            )
        builder.button(text="↩️ Back", callback_data="back")
        builder.adjust(7)
        return builder.as_markup()