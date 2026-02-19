# app/keyboards/inline_menu.py

# Импортируем InlineKeyboardMarkup — объект inline-клавиатуры (кнопки внутри сообщения)
from aiogram.types import InlineKeyboardMarkup  # Тип клавиатуры "внутри сообщения"

# Импортируем InlineKeyboardButton — одна inline-кнопка
from aiogram.types import InlineKeyboardButton  # Описание кнопки

# Импортируем InlineKeyboardBuilder — удобный "конструктор" клавиатуры
from aiogram.utils.keyboard import InlineKeyboardBuilder  # Строитель клавиатуры


def get_main_inline_menu() -> InlineKeyboardMarkup:
    """
    Создаём главное inline-меню:
    - '📦 Скачать остатки'
    - '❓ Задать вопрос'
    """

    # Создаём builder (конструктор)
    builder = InlineKeyboardBuilder()

    # Добавляем кнопку "Скачать остатки"
    # callback_data — скрытая строка, которая придёт нам при нажатии
    builder.add(
        InlineKeyboardButton(
            text="📦 Скачать остатки",      # Текст на кнопке
            callback_data="menu:stock"      # Идентификатор действия
        )
    )

    # Добавляем кнопку "Задать вопрос"
    builder.add(
        InlineKeyboardButton(
            text="❓ Задать вопрос",         # Текст на кнопке
            callback_data="menu:question"   # Идентификатор действия
        )
    )

    # Делаем кнопки в столбик: по 1 кнопке в строке
    builder.adjust(1)

    # Возвращаем готовую клавиатуру
    return builder.as_markup()
def get_question_inline_menu() -> InlineKeyboardMarkup:
    """
    Создаём подменю "Задать вопрос".
    """

    builder = InlineKeyboardBuilder()

    # Кнопка "Продажи"
    builder.add(
        InlineKeyboardButton(
            text="💼 Продажи",
            callback_data="question:sales"
        )
    )

    # Кнопка "Бухгалтерия"
    builder.add(
        InlineKeyboardButton(
            text="📊 Бухгалтерия",
            callback_data="question:accounting"
        )
    )

    # Кнопка "Другое"
    builder.add(
        InlineKeyboardButton(
            text="👤 Другое",
            callback_data="question:other"
        )
    )

    # Кнопка "Назад"
    builder.add(
        InlineKeyboardButton(
            text="⬅ Назад",
            callback_data="menu:back"
        )
    )

    builder.adjust(1)

    return builder.as_markup()

def get_question_inline_menu() -> InlineKeyboardMarkup:
    """
    Создаём подменю "Задать вопрос".
    Кнопки ведут по ссылке в Telegram-чат/личку.
    """

    builder = InlineKeyboardBuilder()

    # Кнопка "Продажи" — ведёт в личку/чат продаж
    builder.add(
        InlineKeyboardButton(
            text="💼 Продажи",
            url="https://t.me/Zuxra_1514"
        )
    )

    # Кнопка "Бухгалтерия" — ведёт в личку/чат бухгалтерии
    builder.add(
        InlineKeyboardButton(
            text="📊 Бухгалтерия",
            url="https://t.me/Dianavabi"
        )
    )

    # Кнопка "Другое" — ведёт к тебе
    builder.add(
        InlineKeyboardButton(
            text="👤 Другое",
            url="https://t.me/toVGera"
        )
    )

    # Кнопка "Назад" — оставляем callback
    builder.add(
        InlineKeyboardButton(
            text="⬅ Назад",
            callback_data="menu:back"
        )
    )

    builder.adjust(1)

    return builder.as_markup()


