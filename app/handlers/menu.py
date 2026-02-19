# app/handlers/menu.py

# Импортируем Router — контейнер для обработчиков
from aiogram import Router

# Импортируем CallbackQuery — событие нажатия inline-кнопки
from aiogram.types import CallbackQuery

# Импортируем F — удобный фильтр для сравнения полей (например data)
from aiogram import F

# Импортируем FSInputFile — правильный тип файла для отправки в aiogram 3
from aiogram.types import FSInputFile

# Импортируем Path для работы с путями
from pathlib import Path


# Создаём router для обработчиков меню
router = Router()

# Папка хранения отчётов
STORAGE_DIR = Path("storage")


# Этот обработчик сработает, когда нажали кнопку с callback_data="menu:stock"
@router.callback_query(F.data == "menu:stock")
async def on_stock_button(callback: CallbackQuery):
    """
    Обработка кнопки "Скачать остатки".
    Ищем последний файл last_report.* и отправляем его.
    """

    # Ищем файл последнего отчёта (любое расширение)
    candidates = list(STORAGE_DIR.glob("last_report.*"))

    # Если файла нет — сообщаем пользователю
    if not candidates:
        # callback.message — исходное сообщение, под которым нажали кнопку
        await callback.message.answer("Пока нет загруженного отчёта. Попроси администратора загрузить файл 🙂")

        # Обязательно "подтверждаем" нажатие, чтобы у Telegram не крутился “часик”
        await callback.answer()
        return

    # Берём первый найденный файл
    report_path = candidates[0]

    # Готовим файл к отправке (aiogram требует FSInputFile)
    document = FSInputFile(path=report_path)

    # Отправляем документ в чат
    await callback.message.answer_document(
        document=document,
        caption="Последний отчёт"
    )

    # Подтверждаем нажатие кнопки
    await callback.answer()
# Импортируем функцию подменю (если ещё не импортирована)
from app.keyboards.inline_menu import get_question_inline_menu


# Обработчик кнопки "Задать вопрос"
@router.callback_query(F.data == "menu:question")
async def on_question_button(callback: CallbackQuery):
    """
    Обработка кнопки 'Задать вопрос'.
    Открываем подменю с выбором отдела.
    """

    # Редактируем текущее сообщение,
    # заменяя текст и клавиатуру
    await callback.message.edit_text(
        "Выберите отдел:",
        reply_markup=get_question_inline_menu()
    )

    # Подтверждаем нажатие
    await callback.answer()
# Обработчик кнопки "Назад"
@router.callback_query(F.data == "menu:back")
async def on_back_button(callback: CallbackQuery):
    """
    Возврат в главное меню.
    """

    # Импортируем главное меню
    from app.keyboards.inline_menu import get_main_inline_menu

    # Редактируем сообщение обратно
    await callback.message.edit_text(
        "Привет! 👋\n\n"
        "Это Ixora Bot.\n"
        "Выберите действие:",
        reply_markup=get_main_inline_menu()
    )

    # Подтверждаем нажатие
    await callback.answer()
