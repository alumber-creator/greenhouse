import asyncio
import logging

from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.__init__ import db, bot
from handlers.admin import dp as r1
from handlers.agro import dp as r2
from handlers.notifications import dp as r3
from handlers.graph import dp as r4
from handlers.video import dp as r5
from services.video import ffmpeg_process

handlers = (r1, r2, r3, r4, r5)


async def main():
    await db.initialize()

    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage(), default=default)

    for router in handlers:
        dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        ffmpeg_process.terminate()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

