# bot/keyboards/graph.py
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
import calendar

from callbacks.graph import DateSelectionCallback, DateModeCallback
from config import Config

# bot/keyboards/graph.py
from aiogram.utils.keyboard import InlineKeyboardBuilder
import calendar


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
    def date_mode_menu():
        builder = InlineKeyboardBuilder()
        builder.button(
            text="📅 Один день",
            callback_data=DateModeCallback(action="single")
        )
        builder.button(
            text="📆 Период",
            callback_data=DateModeCallback(action="period")
        )
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def calendar_menu(year: int, month: int):
        builder = InlineKeyboardBuilder()

        # Заголовок с месяцем и годом
        builder.button(
            text=f"{calendar.month_name[month]} {year}",
            callback_data="ignore"
        )

        # Дни недели
        for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
            builder.button(text=day, callback_data="ignore")

        # Дни месяца
        month_cal = calendar.monthcalendar(year, month)
        for week in month_cal:
            for day in week:
                if day == 0:
                    builder.button(text=" ", callback_data="ignore")
                else:
                    builder.button(
                        text=str(day),
                        callback_data=DateSelectionCallback(
                            action="select",
                            year=year,
                            month=month,
                            day=day
                        )
                    )

        # Навигация
        builder.button(
            text="⬅️",
            callback_data=DateSelectionCallback(
                action="change_month",
                year=year - 1 if month == 1 else year,
                month=12 if month == 1 else month - 1,
                day=0
            )
        )
        builder.button(
            text="➡️",
            callback_data=DateSelectionCallback(
                action="change_month",
                year=year + 1 if month == 12 else year,
                month=1 if month == 12 else month + 1,
                day=0
            )
        )
        builder.button(
            text="✅ Подтвердить",
            callback_data=DateSelectionCallback(
                action="confirm",
                year=year,
                month=month,
                day=0
            )
        )

        builder.adjust(7, *[7] * len(month_cal), 2, 1)
        return builder.as_markup()
