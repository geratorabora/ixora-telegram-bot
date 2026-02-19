# app/handlers/questions.py

# Импортируем Router — контейнер обработчиков для этого файла
from aiogram import Router

# Импортируем CallbackQuery — событие нажатия inline-кнопки
from aiogram.types import CallbackQuery

# Импортируем Message — обычное текстовое сообщение пользователя
from aiogram.types import Message

# Импортируем F — фильтры по полям (например callback_data)
from aiogram import F

# Импортируем FSMContext — объект для работы с "состояниями" (режимами)
from aiogram.fsm.context import FSMContext

# Импортируем базовые классы состояний
from aiogram.fsm.state import State, StatesGroup

# Импортируем главное меню, чтобы потом вернуться назад
from app.keyboards.inline_menu import get_main_inline_menu

# Импортируем список получателей
from app.config import ADMIN_IDS, SALES_CHAT_ID, ACCOUNTING_CHAT_ID


# Создаём router для вопросов
router = Router()


class QuestionFlow(StatesGroup):
    """
    Набор состояний (режимов) для сценария "задать вопрос".
    """
    waiting_for_text = State()  # Состояние: ждём текст вопроса от пользователя


def _pick_target_chat_id(department: str) -> int:
    """
    Определяем, куда отправлять вопрос в зависимости от отдела.
    """

    # Если выбран отдел продаж
    if department == "sales" and SALES_CHAT_ID:
        return int(SALES_CHAT_ID)

    # Если бухгалтерия
    if department == "accounting" and ACCOUNTING_CHAT_ID:
        return int(ACCOUNTING_CHAT_ID)

    # Если "другое" или ID не заданы — отправляем админу
    return int(next(iter(ADMIN_IDS)))

    # Берём первого админа из списка — это ты
    owner_id = int(next(iter(ADMIN_IDS)))


    # Временно отправляем всё тебе
    # (позже сделаем SALES_CHAT_ID и ACCOUNTING_CHAT_ID)
    return owner_id


@router.callback_query(F.data.in_({"question:sales", "question:accounting", "question:other"}))
async def on_department_chosen(callback: CallbackQuery, state: FSMContext):
    """
    Срабатывает, когда пользователь выбирает отдел:
    - 💼 Продажи
    - 📊 Бухгалтерия
    - 👤 Другое

    Дальше просим пользователя написать текст вопроса.
    """

    # Достаём callback_data (например "question:sales")
    data = callback.data

    # Вытаскиваем название отдела после двоеточия
    department = data.split(":")[1]

    # Определяем, куда слать вопрос
    target_chat_id = _pick_target_chat_id(department)

    # Сохраняем в "память состояния" выбранный отдел и адресата
    await state.update_data(department=department, target_chat_id=target_chat_id)

    # Переводим бота в режим ожидания текста вопроса
    await state.set_state(QuestionFlow.waiting_for_text)

    # Просим пользователя написать вопрос
    await callback.message.answer(
        "Напиши свой вопрос одним сообщением.\n"
        "Я передам его в выбранный отдел 🙂"
    )

    # Подтверждаем нажатие кнопки (чтобы у Telegram не крутился индикатор)
    await callback.answer()


@router.message(QuestionFlow.waiting_for_text)
async def on_question_text(message: Message, state: FSMContext):
    """
    Срабатывает, когда пользователь прислал текст вопроса
    в режиме ожидания (waiting_for_text).

    Мы отправляем его адресату и завершаем сценарий.
    """

    # Берём сохранённые ранее данные (отдел и target_chat_id)
    data = await state.get_data()

    # Достаём целевой чат
    target_chat_id = int(data.get("target_chat_id"))

    # Достаём отдел (строка типа sales/accounting/other)
    department = data.get("department", "other")

    # Человеческое название отдела для текста
    dept_name = {
        "sales": "Продажи",
        "accounting": "Бухгалтерия",
        "other": "Другое"
    }.get(department, "Другое")

    # Формируем "шапку" для сотрудника: кто написал и откуда
    header = (
        "📩 Новый вопрос из Ixora Bot\n"
        f"Отдел: {dept_name}\n"
        f"От: {message.from_user.full_name} (id: {message.from_user.id})\n\n"
    )

    # Текст вопроса пользователя
    question_text = message.text or ""

    # Отправляем сообщение адресату (пока что тебе)
    await message.bot.send_message(
        chat_id=target_chat_id,
        text=header + question_text
    )

    # Отвечаем пользователю, что всё отправлено
    await message.answer(
        "Готово! Я передала вопрос ✅\n\n"
        "Если нужно — можешь задать ещё один через меню.",
        reply_markup=get_main_inline_menu()
    )

    # Сбрасываем состояние (выходим из режима ожидания)
    await state.clear()
