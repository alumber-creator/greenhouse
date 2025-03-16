from aiogram import Router, types, F
from aiogram.enums import ParseMode
from database.repositories.user_checks import UserChecksRepository
from keyboards.notifications import build_notifications_kb

router = Router()


@router.callback_query(F.data == "settings.notifications")
async def show_notification_settings(callback: types.CallbackQuery):
    """Обработчик настроек уведомлений"""
    repo = UserChecksRepository(callback.from_user.id)
    checks_state = await repo.get_or_create_checks()

    await callback.message.edit_text(
        "<b>Настройка уведомлений:</b>\n\nВыберите опции",
        reply_markup=build_notifications_kb(checks_state),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@router.callback_query(F.data.startswith("toggle_check:"))
async def toggle_notification_check(callback: types.CallbackQuery):
    """Переключение состояния чекбокса"""
    repo = UserChecksRepository(callback.from_user.id)
    check_name = callback.data.split(":")[1]

    try:
        new_state = await repo.toggle_check(check_name)
        await callback.message.edit_reply_markup(
            reply_markup=build_notifications_kb(new_state)
        )
        await callback.answer()
    except ValueError as e:
        await callback.answer(str(e), show_alert=True)