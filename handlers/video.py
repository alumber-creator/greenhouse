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

    try:
        with open("concat_list.txt", "w") as f:
            f.writelines([f"file '{s}'\n" for s in segments])

        output = "output.mp4"
        subprocess.run([
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", "concat_list.txt",
            "-c", "copy",
            output
        ], check=True)

        if os.path.getsize(output) > 50 * 1024 * 1024:
            compressed = "compressed.mp4"
            subprocess.run([
                "ffmpeg",
                "-i", output,
                "-vf", "scale=640:480",
                "-b:v", "800k",
                compressed
            ], check=True)
            os.remove(output)
            output = compressed

        with open(output, "rb") as video_file:
            await message.reply_video(video_file, caption="Последние 3 минуты")

    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}")
    finally:
        for f in [output, "compressed.mp4", "concat_list.txt"]:
            if os.path.exists(f):
                os.remove(f)
