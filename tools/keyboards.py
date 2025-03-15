from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Keyboard:
    ADMIN = "admin"
    ADMIN_GEN = "admin.gen"

    @staticmethod
    def get_keyboard(key_type: str) -> InlineKeyboardMarkup:
        """Генерирует клавиатуры указанного типа"""
        builder = InlineKeyboardBuilder()
        if key_type == "admin":
            builder.add(types.InlineKeyboardButton(
                text="Тестовая генерация значений датчика",
                callback_data="test.gen")
            )
            builder.add(types.InlineKeyboardButton(
                text="Назад",
                callback_data="start")
            )
            builder.adjust(1, 1)

        if key_type == "admin.gen":
            builder.add(types.InlineKeyboardButton(
                text="Тестовая генерация значений датчика",
                callback_data="test.gen")
            )
            builder.add(types.InlineKeyboardButton(
                text="Назад",
                callback_data="admin_panel")
            )
            builder.adjust(1, 1)

        return builder.as_markup()
