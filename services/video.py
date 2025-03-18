from config import Config
import os
import asyncio
import subprocess
import glob
from datetime import datetime

def start_ffmpeg_recording():
    """Запуск фоновой записи видео сегментами"""
    os.makedirs(Config.TEMP_DIR, exist_ok=True)
    command = [
        "ffmpeg",
        "-i", "/dev/video0",           # Источник видео (может отличаться)
        "-c:v", "libx264",             # Кодек
        "-f", "segment",               # Формат сегментов
        "-strftime", "1",              # Использовать время в имени файла
        "-segment_time", "10",         # Длительность сегмента (сек)
        "-reset_timestamps", "1",      # Сброс таймстемпов
        f"{Config.TEMP_DIR}/%Y%m%d%H%M%S.mp4" # Шаблон имени файла
    ]
    return subprocess.Popen(command, stderr=subprocess.DEVNULL)

ffmpeg_process = start_ffmpeg_recording()

async def run_command(command):
    """Асинхронный запуск команд"""
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await process.wait()
    return process.returncode == 0

async def cleanup_old_files(threshold):
    """Удаление старых файлов"""
    for path in glob.glob(f"{Config.TEMP_DIR}/*.mp4"):
        filename = os.path.basename(path)
        try:
            dt = datetime.strptime(filename, "%Y%m%d%H%M%S.mp4")
        except ValueError:
            continue
        if dt < threshold:
            os.remove(path)



