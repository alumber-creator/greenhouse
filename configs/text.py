from aiogram.types import CallbackQuery

from configs.config import Config
from database import Database


class Text:
    ADMIN = "<b>Панель администратора</b> \n\nДля отправки уведомления, используйте команду /send_notification"
    ADMIN_TEST_GEN = "<b>Панель администратора</b> \n\nДанные успешно сгенерированы"
    ADMIN_WAIT_GEN = "Идёт генерация, пожалуйста, подождите..."

    AGRO_START = "Приветствуем вас в боте для управления автономным агрокомплексом"

    NOTIFICATION_SETTINGS = "<b>Настройка уведомлений:</b>\n\nВыберите опции"
    NOTIFICATION_TEXT_CHOOSE = "📝 Введите текст уведомления:"
    NOTIFICATION_LEVEL_CHOOSE = "🔢 Выберите уровень уведомления (1-4):"
    NOTIFICATION_SUCCESS = "✅ Уведомление успешно отправлено!"
    NOTIFICATION_CANCEL = "❌ Отправка уведомления отменена"

    ERROR_ADMIN_RESTRICTED = "Запрещен доступ пользователю ниже ранга admin"
    ERROR_NOTIFICATION = f"⚠️ Текст уведомления слишком длинный. Максимум {Config.MAX_TEXT_LENGTH} символов."

    @staticmethod
    async def get_text_agro_settings(callback: CallbackQuery, db: Database) -> str:
        users = await db.users.get_users(conditions="user_id = ?", params=(callback.from_user.id,))
        user = users[0]
        return f"""
<b>Пользователь</b> {callback.from_user.mention_html()}
<b>ID</b>: {callback.from_user.id}
<b>Роль в системе</b>: {user.role}
<b>Аккаунт зарегистрирован</b>: {user.created_at} 
        """
