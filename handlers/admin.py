from aiogram import types, F, Router
from aiogram.enums import ParseMode

from tools.data_generation import DataGen
from tools.keyboards import Keyboard
from tools.text import Text as txt

dp = Router()


@dp.callback_query(F.data == "admin.panel")
async def admin_panel(callback: types.CallbackQuery):
    """Отображает интерфейс администраторской панели с кнопками управления"""
    keyboard = await Keyboard.get_keyboard(Keyboard.ADMIN)
    await callback.answer()
    await callback.message.edit_text(txt.ADMIN, reply_markup=keyboard, parse_mode=ParseMode.HTML)


@dp.callback_query(F.data == "test.gen")
async def test_gen(callback: types.CallbackQuery):
    """Запускает процесс тестовой генерации данных"""
    keyboard = await Keyboard.get_keyboard(Keyboard.ADMIN_GEN)
    await callback.answer()
    await callback.message.edit_text(txt.ADMIN_WAIT_GEN)
    await DataGen.test_generation()
    await callback.message.edit_text(txt.ADMIN_TEST_GEN, reply_markup=keyboard, parse_mode=ParseMode.HTML)



