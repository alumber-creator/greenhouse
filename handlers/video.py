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
    await message.reply("Обрабатываю запрос...")

    segments = recorder.get_segments()
    if not segments:
        await message.reply("Нет доступных записей")
        return

    output = "output.mp4"
    compressed = "compressed.mp4"
    final_file = None

    try:
        # Создаем список для склейки
        with open("concat_list.txt", "w") as f:
            f.writelines([f"file '{s}'\n" for s in segments])

        # Склеиваем видео через ffmpeg
        result = subprocess.run([
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", "concat_list.txt",
            "-c", "copy",
            output
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"FFmpeg error: {result.stderr}")

        # Проверяем размер файла
        if os.path.getsize(output) > 50 * 1024 * 1024:
            # Сжимаем видео
            result = subprocess.run([
                "ffmpeg",
                "-i", output,
                "-vf", "scale=640:480",
                "-b:v", "800k",
                compressed
            ], capture_output=True, text=True)

            if result.returncode != 0:
                raise Exception(f"Compression error: {result.stderr}")

            final_file = compressed
        else:
            final_file = output

        # Проверяем существование файла
        if not os.path.exists(final_file):
            raise Exception("Final video file not created")

        # Отправляем видео с использованием InputFile
        with open(final_file, "rb") as video_file:
            input_file = InputFile(video_file, filename=final_file)
            await message.reply_video(
                video=input_file,
                caption="Последние 3 минуты"
            )

    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}")
    finally:
        # Очистка временных файлов
        temp_files = [output, compressed, "concat_list.txt"]
        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)

