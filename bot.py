import asyncio
import hashlib
import logging
import os

from aiogram.exceptions import TelegramConflictError, TelegramBadRequest

from app.bot import create_bot, create_dispatcher
from app.config import BOT_TOKEN
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


def _polling_lock_key() -> int:
    # Ключ завязан на токен, чтобы test/prod не блокировали друг друга,
    # даже если используют одну Postgres-базу.
    digest = hashlib.blake2b(BOT_TOKEN.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big", signed=False) & 0x7FFFFFFFFFFFFFFF


async def acquire_polling_lock():
    db_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
    if not db_url:
        logger.warning("DATABASE_URL is not set; polling lock is disabled")
        return None

    import psycopg

    lock_key = _polling_lock_key()
    while True:
        try:
            conn = await asyncio.to_thread(psycopg.connect, db_url)
            acquired = await asyncio.to_thread(
                lambda: conn.execute("SELECT pg_try_advisory_lock(%s)", (lock_key,)).fetchone()[0]
            )
            if acquired:
                logger.info("Acquired Telegram polling lock")
                return conn
            await asyncio.to_thread(conn.close)
            logger.warning("Another bot instance holds polling lock; retrying in 30s...")
        except Exception as e:
            logger.warning("Cannot acquire polling lock: %s — retrying in 30s...", e)
        await asyncio.sleep(30)


async def release_polling_lock(conn) -> None:
    if not conn:
        return
    try:
        lock_key = _polling_lock_key()
        await asyncio.to_thread(conn.execute, "SELECT pg_advisory_unlock(%s)", (lock_key,))
        await asyncio.to_thread(conn.close)
        logger.info("Released Telegram polling lock")
    except Exception as e:
        logger.warning("Cannot release polling lock cleanly: %s", e)

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

    lock_conn = await acquire_polling_lock()

    # Ждём пока не сможем подключиться (другой инстанс мог не успеть остановиться)
    while True:
        try:
            await bot.get_updates(offset=-1, limit=1, timeout=0)
            break
        except (TelegramConflictError, TelegramBadRequest) as e:
            logger.warning(f"Cannot start polling yet: {e} — retrying in 60s...")
            await asyncio.sleep(60)

    try:
        await dp.start_polling(bot)
    finally:
        await release_polling_lock(lock_conn)


# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(main())  # Запускаем асинхронную функцию main()
