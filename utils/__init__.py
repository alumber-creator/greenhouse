import logging

from aiogram import types

from database import Database
from config.text import Text as txt


class Tools:
    @staticmethod
    async def is_admin(telegram_id: int, db: Database):
        admins = await db.users.get_users(
            conditions="role = ?",
            params=("admin",)
        )
        return any(telegram_id == admin.user_id for admin in admins)

    @classmethod
    async def check_admin(cls, callback: types.CallbackQuery, db: Database):
        if not await cls.is_admin(callback.from_user.id, db):
            await callback.answer()
            logging.debug(f"{txt.ERROR_ADMIN_RESTRICTED} {callback.from_user.username}")
            await callback.message.delete()
            return True
        else:
            await callback.answer()
            return False