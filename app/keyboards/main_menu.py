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

    # Собираем клавиатуру из двух кнопок (в один ряд)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[btn_stock, btn_question]],  # Матрица кнопок: 1 строка, 2 кнопки
        resize_keyboard=True,  # Подгоняем размер клавиатуры под телефон
        input_field_placeholder="Выберите действие…"  # Подсказка в поле ввода
    )

    # Возвращаем готовую клавиатуру
    return keyboard
