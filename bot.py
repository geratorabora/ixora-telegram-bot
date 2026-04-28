import asyncio
import logging

from aiogram.exceptions import TelegramConflictError

from app.bot import create_bot, create_dispatcher
from app.handlers.start import router as start_router
from app.handlers.id import router as id_router
from app.handlers.upload import router as upload_router
from app.handlers.get import router as get_router
from app.handlers.menu import router as menu_router
from app.handlers.questions import router as questions_router
from pathlib import Path
from datetime import datetime, timedelta
import shutil

logger = logging.getLogger(__name__)

STORAGE_DIR = Path("storage")
ARCHIVE_DIR = STORAGE_DIR / "archive"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

def cleanup_old_archives(days: int = 7) -> int:
    cutoff = datetime.now() - timedelta(days=days)
    deleted = 0

    if not ARCHIVE_DIR.exists():
        return 0

    for user_dir in ARCHIVE_DIR.iterdir():
        if not user_dir.is_dir():
            continue

        for slot in user_dir.iterdir():
            if not slot.is_dir():
                continue

            mtime = datetime.fromtimestamp(slot.stat().st_mtime)
            if mtime < cutoff:
                shutil.rmtree(slot, ignore_errors=True)
                deleted += 1

    return deleted

async def main():
    bot = create_bot()
    dp = create_dispatcher()

    dp.include_router(start_router)
    dp.include_router(id_router)
    dp.include_router(upload_router)
    dp.include_router(get_router)
    dp.include_router(menu_router)
    dp.include_router(questions_router)

    deleted = cleanup_old_archives(days=7)
    if deleted:
        print(f"Archive cleanup: deleted {deleted} folder(s) older than 7 days")

    while True:
        try:
            await dp.start_polling(bot)
            break
        except TelegramConflictError:
            logger.warning("Another bot instance is running, retrying in 30s...")
            await asyncio.sleep(30)


# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(main())  # Запускаем асинхронную функцию main()
