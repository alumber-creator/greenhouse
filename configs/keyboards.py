from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Dict, List, Tuple

from database import Database
from tools.tool import Tools


class Keyboard:
    class Types:
        ADMIN = "admin"
        ADMIN_GEN = "admin.gen"
        AGRO_START = "agro.start"
        AGRO_SETTINGS = "agro.settings"

    # Конфигурация кнопок для разных типов клавиатур
    _KEYBOARD_CONFIG: Dict[str, List[Tuple[str, str]]] = {
        Types.ADMIN: [
            ("Тестовая генерация значений датчика", "test.gen"),
            ("Назад", "start")
        ],
        Types.ADMIN_GEN: [
            ("Тестовая генерация значений датчика", "test.gen"),
            ("Назад", "admin.panel")
        ],
        Types.AGRO_SETTINGS: [
            ("Настройка уведомлений", "settings.notifications"),
            ("Назад", "start")
        ],
        Types.AGRO_START: [
            ("Настройки", "settings"),
            ("Админ панель", "admin.panel"),
            ("Панель управления", "panel")
        ]
    }

    @classmethod
    async def get_keyboard(
            cls,
            key_type: str,
            db: Database = None,
            telegram_id: int = None
    ) -> InlineKeyboardMarkup:
        """
        Генерирует инлайн-клавиатуру указанного типа

        :param key_type: Тип клавиатуры из Keyboard.Types
        :param telegram_id: Опциональный ID пользователя для проверки прав
        :param db: Объект базы данных
        :return: Объект InlineKeyboardMarkup
        """
        builder = InlineKeyboardBuilder()
        buttons_config = cls._KEYBOARD_CONFIG.get(key_type, [])

        # Для agro.start добавляем проверку админских прав
        if key_type == cls.Types.AGRO_START:
            buttons_config = await cls._handle_agro_start(buttons_config, telegram_id, db)

        for text, callback_data in buttons_config:
            builder.add(types.InlineKeyboardButton(
                text=text,
                callback_data=callback_data
            ))

        # Автоматическое выравнивание кнопок
        builder.adjust(*cls._get_adjust_pattern(key_type))
        return builder.as_markup()

    @classmethod
    async def _handle_agro_start(
            cls,
            buttons: List[Tuple[str, str]],
            telegram_id: int,
            db: Database
    ) -> List[Tuple[str, str]]:
        """Обрабатывает специальный случай для agro.start"""
        filtered_buttons = [buttons[0]]  # Всегда добавляем Настройки
        if await Tools.is_admin(telegram_id, db):
            filtered_buttons.extend(buttons[1:])
        return filtered_buttons

    @staticmethod
    def _get_adjust_pattern(key_type: str) -> Tuple[int, ...]:
        """Возвращает шаблон выравнивания кнопок"""
        adjust_patterns = {
            Keyboard.Types.AGRO_START: (1, 1, 1),
            Keyboard.Types.ADMIN: (1, 1),
            Keyboard.Types.ADMIN_GEN: (1, 1),
            Keyboard.Types.AGRO_SETTINGS: (1, 1)
        }
        return adjust_patterns.get(key_type, (1,))


