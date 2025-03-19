import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
API_TOKEN = 'YOUR_BOT_TOKEN'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['video'])
async def send_video(message: types.Message):
    try:
        # Отправляем видеофайл
        video = types.InputFile("output.mp4")
        await message.answer_video(video)
        logging.info(f"Video sent to {message.from_user.id}")
    except FileNotFoundError:
        await message.answer("❌ Файл video.mp4 не найден")
        logging.error("File output.mp4 not found")
    except Exception as e:
        await message.answer("⚠️ Произошла ошибка при отправке видео")
        logging.error(f"Error sending video: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)