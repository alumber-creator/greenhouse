import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from configs.config import db
from handlers.admin import dp as r1
from handlers.agro import dp as r2


handlers = (r1, r2)

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    raise ValueError("Токен бота не найден в переменных окружения!")



async def main():
    bot = Bot(TOKEN)

    await db.initialize()
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage(), default=default)

    for router in handlers:
        dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
