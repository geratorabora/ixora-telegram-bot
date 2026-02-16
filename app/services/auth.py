# Импортируем список администраторов из конфигурационного файла
# ADMIN_IDS — это множество (set) чисел Telegram ID
from app.config import ADMIN_IDS


def is_admin(user_id: int) -> bool:
    """
    Функция проверяет, является ли пользователь администратором.

    user_id: Telegram ID пользователя (число)
    return: True если админ, иначе False
    """

    # Проверяем, содержится ли переданный ID в списке админов
    return user_id in ADMIN_IDS
