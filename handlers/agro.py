from aiogram import Router, F

dp = Router()

@dp.callback_query(F.data == "start")
async def start(...):
    """Главное меню с динамическими кнопками"""

@dp.message(Command("start"))
async def cmd_start(...):
    """Обработчик команды /start"""

@dp.callback_query(F.data == "settings")
async def settings(...):
    """Персональные настройки пользователя"""

@dp.callback_query(F.data == "panel")
async def panel(...):
    """Центр управления агрокомплексом"""

