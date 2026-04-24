import os
from dotenv import load_dotenv

# 0) Определяем: мы на Railway?
is_railway = bool(os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID"))

# 1) По умолчанию запускаемся в test (локально)
app_env = os.getenv("APP_ENV", "test").lower()

# 2) Загружаем env-файл ТОЛЬКО локально (не на Railway)
if not is_railway:
    # test -> .env.test, prod -> .env, иначе .env.<env>
    if app_env == "prod":
        env_file = ".env"
    elif app_env == "test":
        env_file = ".env.test"
    else:
        env_file = f".env.{app_env}"

    load_dotenv(dotenv_path=env_file, override=False)
    print(f"APP_ENV= {app_env}  env_file= {env_file}  BOT_TOKEN exists= {bool(os.getenv('BOT_TOKEN'))}")
else:
    print(f"APP_ENV= {app_env} (Railway) BOT_TOKEN exists= {bool(os.getenv('BOT_TOKEN'))}")
from aiogram import Bot, Dispatcher
from .config import BOT_TOKEN

def create_bot() -> Bot:
    return Bot(token=BOT_TOKEN)

def create_dispatcher() -> Dispatcher:
    return Dispatcher()
