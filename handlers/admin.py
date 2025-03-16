from aiogram import types, F, Router
from aiogram.enums import ParseMode

from config import db
from utils.data_generation import DataGen
from config.keyboards import Keyboard
from config.text import Text as txt
from utils import Tools


dp = Router()



@dp.callback_query(F.data == "admin.panel")
async def admin_panel(callback: types.CallbackQuery):
    """Отображает интерфейс администраторской панели с кнопками управления"""
    if await Tools.check_admin(callback, db): return
    keyboard = await Keyboard.get_keyboard(Keyboard.Types.ADMIN)
    await callback.message.edit_text(txt.ADMIN, reply_markup=keyboard, parse_mode=ParseMode.HTML)


@dp.callback_query(F.data == "test.gen")
async def test_gen(callback: types.CallbackQuery):
    """Запускает процесс тестовой генерации данных"""
    if await Tools.check_admin(callback, db): return
    keyboard = await Keyboard.get_keyboard(Keyboard.Types.ADMIN_GEN)
    await callback.message.edit_text(txt.ADMIN_WAIT_GEN)
    await DataGen.test_generation(db)
    await callback.message.edit_text(txt.ADMIN_TEST_GEN, reply_markup=keyboard, parse_mode=ParseMode.HTML)



