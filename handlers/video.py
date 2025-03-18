from datetime import datetime, timedelta
from aiogram.types import Message, InputFile
from aiogram import Router
from aiogram.filters import Command

from config import Config
import glob
import os

from services.video import run_command, cleanup_old_files
dp = Router()

@dp.message(Command("video"))
async def cmd_get_video(message: Message):
    try:
        now = datetime.now()
        threshold = now - timedelta(minutes=Config.BUFFER_DURATION)

        # Поиск актуальных сегментов
        segments = []
        for path in glob.glob(f"{Config.TEMP_DIR}/*.mp4"):
            filename = os.path.basename(path)
            try:
                dt = datetime.strptime(filename, "%Y%m%d%H%M%S.mp4")
            except ValueError:
                continue
            if dt >= threshold:
                segments.append((dt, path))
        if not segments:
            return await message.reply("⚠️ Видео не найдено")

            # Сортировка и выбор файлов
        segments.sort()
        video_files = [path for _, path in segments]

        # Создание списка для конкатенации
        list_file = os.path.join(Config.TEMP_DIR, "concat.txt")
        with open(list_file, "w") as f:
            for file in video_files:
                f.write(f"file '{os.path.basename(file)}'\n")
        output_file = os.path.join(Config.TEMP_DIR, "output.mp4")
        success = await run_command([
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            output_file
        ])
        if not success:
            return await message.reply("❌ Ошибка обработки видео")

        # Отправка видео
        await message.reply_video(
            video=InputFile(output_file),
            caption="🎥 Последние 3 минуты:"
        )

        # Очистка временных файлов
        os.remove(list_file)
        os.remove(output_file)
        await cleanup_old_files(threshold)

    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {str(e)}")