import os

from aiogram import Bot
from dotenv import load_dotenv

from database import Database


class Config:
    SENSORS = ["temperature", "humidity", "light"]

    CHECK_OPTIONS = [
        ("check1", "Уведомления о критических ситуациях"),
        ("check2", "Уведомления о выполнении операций"),
        ("check3", "Уведомления с рекомендациями"),
    ]

    MAX_TEXT_LENGTH = 4000

    SEGMENT_DURATION = 60  # Длительность сегмента в секундах (1 минута)
    MAX_SEGMENTS = 3  # Хранить последние 3 сегмента (3 минуты)
    RESOLUTION = (640, 480)  # Разрешение видео
    FPS = 30  # Кадров в секунду


db = Database(Config.SENSORS)
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    raise ValueError("Токен бота не найден в переменных окружения!")
bot = Bot(TOKEN)

