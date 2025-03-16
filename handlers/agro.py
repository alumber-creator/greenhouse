from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

from config.keyboards import Keyboard
from config.text import Text as txt, Text
from config import db
from database.models import User

dp = Router()


@dp.callback_query(F.data == "start")
async def start(callback: types.CallbackQuery):
    """Главное меню с динамическими кнопками"""
    await db.users.add_user(User(user_id=int(callback.from_user.id), username=callback.from_user.username))
    keyboard = await Keyboard.get_keyboard(Keyboard.Types.AGRO_START, db, callback.from_user.id)
    await callback.answer()
    await callback.message.edit_text(txt.AGRO_START, reply_markup=keyboard, parse_mode=ParseMode.HTML)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    await db.users.add_user(User(user_id=int(message.from_user.id), username=message.from_user.username))
    keyboard = await Keyboard.get_keyboard(Keyboard.Types.AGRO_START, db, message.from_user.id)
    await message.answer(txt.AGRO_START, reply_markup=keyboard, parse_mode=ParseMode.HTML)


@dp.callback_query(F.data == "settings")
async def settings(callback: types.CallbackQuery):
    """Персональные настройки пользователя"""
    await callback.answer()
    keyboard = await Keyboard.get_keyboard(Keyboard.Types.AGRO_SETTINGS, db)
    await callback.message.edit_text(text=await Text.get_text_agro_settings(callback, db), reply_markup=keyboard, parse_mode=ParseMode.HTML)


@dp.callback_query(F.data == "panel")
async def panel(callback: types.CallbackQuery):
    """Центр управления агрокомплексом"""

