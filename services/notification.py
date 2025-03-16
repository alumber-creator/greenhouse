from aiogram import Bot
from typing import Optional

from config import db


class NotificationService:
    @staticmethod
    async def send_notification(
        text: str,
        level: int,
        bot: Bot
    ) -> Optional[str]:
        try:
            if level != 4:
                users = await db.users.get_checks(level)
            else:
                users = await db.users.get_users()
            for user in users:
                await bot.send_message(user.user_id, text=text)
            return None
        except Exception as e:
            return str(e)

