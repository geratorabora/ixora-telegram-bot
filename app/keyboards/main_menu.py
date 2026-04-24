# app/keyboards/main_menu.py

# Импортируем тип клавиатуры ReplyKeyboardMarkup (клавиатура под строкой ввода)
from aiogram.types import ReplyKeyboardMarkup  # Тип "обычной" клавиатуры
# Импортируем KeyboardButton (одна кнопка)
from aiogram.types import KeyboardButton  # Описание кнопки


def get_main_menu() -> ReplyKeyboardMarkup:
    # Создаём кнопку "Остатки"
    btn_stock = KeyboardButton(text="📦 загрузить остатки")

    # Создаём кнопку "❓ Вопрос"
    btn_question = KeyboardButton(text="❓ задать вопрос")

    btn_staff = KeyboardButton(text="👩‍💼 Для сотрудников")  # Новая кнопка: раздел с внутренними инструментами

    # Собираем клавиатуру из двух кнопок (в один ряд)
    keyboard = ReplyKeyboardMarkup(
                keyboard=[  # Матрица кнопок: список рядов (каждый ряд — список кнопок)
            [btn_stock],     # 1-й ряд: "📦 загрузить остатки"
            [btn_question],  # 2-й ряд: "❓ задать вопрос"
            [btn_staff],     # 3-й ряд: "👩‍💼 Для сотрудников"
        ],
        resize_keyboard=True,  # Подгоняем размер клавиатуры под телефон
        input_field_placeholder="Выберите действие…"  # Подсказка в поле ввода
    )

    # Возвращаем готовую клавиатуру
    return keyboard
