# Router — контейнер обработчиков
from aiogram import Router

# Bot нужен, чтобы скачивать файлы из Telegram
from aiogram import Bot

# Message — входящее сообщение
from aiogram.types import Message

# F — фильтры, например "только документы"
from aiogram import F

# Проверка прав
from app.services.auth import is_admin

# Работа с путями/файлами
from pathlib import Path


# Роутер этого модуля
router = Router()

# Папка, где храним файлы
STORAGE_DIR = Path("storage")

# Убеждаемся, что папка есть
STORAGE_DIR.mkdir(exist_ok=True)


@router.message(F.document)
async def upload_report(message: Message, bot: Bot):
    """
    Срабатывает, когда пользователю присылает боту документ.
    Скачивает файл и сохраняет как последнюю версию отчёта.
    """

    # Telegram ID отправителя
    user_id = message.from_user.id

    # Если не админ — запретить загрузку
    if not is_admin(user_id):
        await message.answer("Загружать отчёт могут только администраторы.")
        return

    # Документ (файл), который прислал пользователь
    doc = message.document

    # Имя файла (как у пользователя)
    filename = doc.file_name

    # Расширение файла (например .xlsx)
    ext = Path(filename).suffix.lower()

    # Разрешённые расширения
    allowed_ext = {".xlsx", ".xls", ".csv", ".pdf"}

    # Если расширение не подходит — отклоняем
    if ext not in allowed_ext:
        await message.answer("Принимаю только xlsx/xls/csv/pdf.")
        return

    # Получаем объект файла в Telegram (с путём file_path)
    file = await bot.get_file(doc.file_id)

    # Временный путь, куда сначала скачаем файл
    temp_path = STORAGE_DIR / f"temp{ext}"

    # Скачиваем файл из Telegram на диск сервера/компа
    await bot.download_file(file.file_path, destination=temp_path)

    # Удаляем старые версии last_report.* (если были)
    for old in STORAGE_DIR.glob("last_report.*"):
        old.unlink(missing_ok=True)

    # Финальное имя файла "последний отчёт"
    final_path = STORAGE_DIR / f"last_report{ext}"

    # Переименовываем temp-файл в last_report.*
    temp_path.rename(final_path)

    # Сообщаем об успехе
    await message.answer(
        "Отчёт обновлён ✅\n"
        "Теперь любой может скачать его командой /get"
    )
