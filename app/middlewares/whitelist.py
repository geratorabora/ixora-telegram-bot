from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from config.access import WHITELIST


class WhitelistMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict
    ) -> Any:
        user_id = None

        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id

        elif isinstance(event, CallbackQuery) and event.from_user:
            user_id = event.from_user.id

        # Если пользователь не в whitelist — мягкий отказ
        if user_id not in WHITELIST:

            if isinstance(event, Message):
                await event.answer("Staff only")
                return

            elif isinstance(event, CallbackQuery):
                await event.answer("Staff only", show_alert=True)
                return

        return await handler(event, data)