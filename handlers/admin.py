from aiogram import types, F, Router
from aiogram.enums import ParseMode

from configs.config import db
from tools.data_generation import DataGen
from configs.keyboards import Keyboard
from configs.text import Text as txt
from tools.tool import Tools


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



