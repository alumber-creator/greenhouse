from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import db, Config, bot
from database.repositories.user_checks import UserChecksRepository
from config.keyboards import Keyboard as kb
from services.notification import NotificationService
from states.notification import NotificationStates
from utils import Tools
from config.text import Text as txt

dp = Router()


@dp.callback_query(F.data == "settings.notifications")
async def show_notification_settings(callback: types.CallbackQuery):
    """Обработчик настроек уведомлений"""
    repo = UserChecksRepository(callback.from_user.id)
    checks_state = await repo.get_or_create_checks()
    await callback.message.edit_text(
        txt.NOTIFICATION_SETTINGS,
        reply_markup=kb.build_notifications_kb(checks_state),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("toggle_check:"))
async def toggle_notification_check(callback: types.CallbackQuery):
    """Переключение состояния чекбокса"""
    repo = UserChecksRepository(callback.from_user.id)
    check_name = callback.data.split(":")[1]

    try:
        new_state = await repo.toggle_check(check_name)
        await callback.message.edit_reply_markup(
            reply_markup=kb.build_notifications_kb(new_state)
        )
        await callback.answer()
    except ValueError as e:
        await callback.answer(str(e), show_alert=True)


@dp.message(Command("send_notification"))
async def cmd_send_notification(message: types.Message, state: FSMContext):
    if not await Tools.is_admin(message.from_user.id, db):
        await message.answer(txt.ERROR_ADMIN_RESTRICTED)
        return

    await message.answer(txt.NOTIFICATION_TEXT_CHOOSE)
    await state.set_state(NotificationStates.waiting_for_text)


@dp.message(NotificationStates.waiting_for_text)
async def process_text(message: types.Message, state: FSMContext):
    if len(message.text) > Config.MAX_TEXT_LENGTH:
        await message.answer(txt.ERROR_NOTIFICATION)
        return

    await state.update_data(text=message.text)
    await message.answer(
        txt.NOTIFICATION_LEVEL_CHOOSE,
        reply_markup=kb.build_levels_kb()
    )
    await state.set_state(NotificationStates.waiting_for_level)


@dp.callback_query(F.data.startswith("notif_level_"), NotificationStates.waiting_for_level)
async def process_level(
        callback: types.CallbackQuery,
        state: FSMContext,
):
    level = int(callback.data.split('_')[2])
    data = await state.get_data()

    await NotificationService.send_notification(data['text'], level, bot)
    await callback.message.edit_text(txt.NOTIFICATION_SUCCESS)

    await state.clear()


@dp.callback_query(F.data == "notif_cancel", NotificationStates.waiting_for_level)
async def cancel_notification(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(txt.NOTIFICATION_CANCEL)