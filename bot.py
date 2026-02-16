import asyncio  # Модуль для работы с асинхронным запуском

from app.bot import create_bot, create_dispatcher  # Фабрики создания bot и dispatcher

# Импортируем router'ы из наших модулей
from app.handlers.start import router as start_router
from app.handlers.id import router as id_router
from app.handlers.upload import router as upload_router  
from app.handlers.get import router as get_router # <-- новый импорт



async def main():
    # Создаём экземпляр бота
    bot = create_bot()

    # Создаём диспетчер (он управляет обработкой сообщений)
    dp = create_dispatcher()

    # Подключаем роутеры (порядок не критичен)
    dp.include_router(start_router)
    dp.include_router(id_router)
    dp.include_router(upload_router)
    dp.include_router(get_router)  # <-- подключаем обработчик загрузки

    # Запускаем бесконечный polling (бот начинает слушать Telegram)
    await dp.start_polling(bot)


# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(main())  # Запускаем асинхронную функцию main()
