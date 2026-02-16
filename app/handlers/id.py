from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("id"))
async def id_handler(message: Message):
    await message.answer(f"Твой Telegram ID: {message.from_user.id}")
