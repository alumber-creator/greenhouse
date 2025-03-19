from datetime import datetime, timedelta
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from aiogram import Router
from aiogram.filters import Command
import subprocess
from aiogram import types, F, Router
from config import Config
import os

from services.video import recorder

dp = Router()
@dp.callback_query(F.data == "video")
async def handle_video_request(callback: types.CallbackQuery):
    message=callback.message
    await message.edit_text(text="Обработка запроса...")

    segments = recorder.get_segments()
    if not segments:
        await message.edit_text(text="Нет доступных записей")
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
        await message.delete()
        await message.reply_video(
            video=FSInputFile(final_file),
            caption="Последние 3 минуты"
        )

    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}")


