from datetime import datetime, timedelta
from aiogram.types import Message, InputFile
from aiogram import Router
from aiogram.filters import Command
import subprocess

from config import Config
import os

from services.video import recorder

dp = Router()

@dp.message(Command("video"))
async def handle_video_request(message: Message):
    await message.reply("Обработка запроса...")

    segments = recorder.get_segments()
    if not segments:
        await message.reply("Нет доступных записей")
        return

    output = "output.mp4"
    compressed = "compressed.mp4"
    final_file = None

    try:
        # Создание списка для склейки
        with open("concat_list.txt", "w") as f:
            f.writelines([f"file '{s}'\n" for s in segments])

        # Склейка видео
        subprocess.run([
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", "concat_list.txt",
            "-c", "copy",
            output
        ], check=True)

        # Сжатие при необходимости
        if os.path.getsize(output) > 50 * 1024 * 1024:
            subprocess.run([
                "ffmpeg",
                "-i", output,
                "-vf", "scale=640:480",
                "-b:v", "800k",
                compressed
            ], check=True)
            final_file = compressed
        else:
            final_file = output

        # Отправка видео с использованием правильного InputFile
        await message.reply_video(
            video=InputFile(final_file),
            caption="Последние 3 минуты"
        )

    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}")
    finally:
        # Удаление временных файлов
        for f in [output, compressed, "concat_list.txt"]:
            if os.path.exists(f):
                os.remove(f)


