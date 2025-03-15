from tools.database import Database


class Tools:
    @staticmethod
    async def is_admin(telegram_id: int):
        admins = await Database.get_users(
            conditions="role = ?",
            params=("admin",)
        )
        return True if telegram_id in admins[4] else False