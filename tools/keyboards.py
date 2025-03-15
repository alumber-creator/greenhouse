from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Keyboard:
    ADMIN = "admin"
    ADMIN_GEN = "admin.gen"

    @staticmethod
    async def get_keyboard(key_type: str, telegram_id: int = None) -> InlineKeyboardMarkup:
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

        if key_type == "agro.start":
            builder.add(types.InlineKeyboardButton(
                text="Настройки",
                callback_data="settings")
            )
            if is_admin(telegram_id):
                builder.add(types.InlineKeyboardButton(
                    text="Админ панель",
                    callback_data="admin_panel")
                )
                builder.add(types.InlineKeyboardButton(
                    text="Панель управления",
                    callback_data="panel")
                )
            builder.adjust(1, 1, 1)

        return builder.as_markup()


