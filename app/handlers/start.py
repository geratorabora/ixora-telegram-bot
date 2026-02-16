from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
    "Привет! 👋\n\n"
    "Это Ixora Bot.\n"
    "Здесь можно скачать текущие остатки по команде /get"
)

