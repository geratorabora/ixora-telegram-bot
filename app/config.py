import os  # Доступ к переменным окружения (APP_ENV и т.п.)
from dotenv import load_dotenv  # Утилита, которая читает .env файлы


# 1) Определяем, в какой среде запускаемся:
#    - если APP_ENV не задана, считаем, что это production ("prod")
app_env = os.getenv("APP_ENV", "prod").lower()

# 2) Выбираем, какой env-файл загружать
#    - prod -> .env
#    - test -> .env.test
env_file = ".env" if app_env == "prod" else f".env.{app_env}"

# 3) Загружаем выбранный env-файл
#    override=False означает: если переменная уже есть в окружении,
#    мы её НЕ перезатираем значением из файла
load_dotenv(dotenv_path=env_file, override=False)


# 4) Читаем токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 5) Если токена нет — это критическая ошибка: бот не запустится
if not BOT_TOKEN:
    raise ValueError(f"BOT_TOKEN не найден. Проверь файл {env_file} или переменные окружения.")


# 6) Читаем список админов (строка с числами через запятую)
raw_admins = os.getenv("ADMIN_IDS", "")

# 7) Превращаем строку в множество (set) чисел для быстрой проверки прав
ADMIN_IDS = set()
if raw_admins:
    ADMIN_IDS = {int(admin_id.strip()) for admin_id in raw_admins.split(",") if admin_id.strip()}
# ==========================
# ID сотрудников для маршрутизации вопросов
# ==========================

# Берём ID отдела продаж из переменных окружения
SALES_CHAT_ID = os.getenv("SALES_CHAT_ID")

# Берём ID бухгалтерии
ACCOUNTING_CHAT_ID = os.getenv("ACCOUNTING_CHAT_ID")


