from aiogram import Bot, Dispatcher
from .config import BOT_TOKEN

def create_bot() -> Bot:
    return Bot(token=BOT_TOKEN)

def create_dispatcher() -> Dispatcher:
    return Dispatcher()
