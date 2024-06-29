import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers import Handlers
from config import BOT_TOKEN, DATABASE_URL
from models import Base, engine


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/vacancies", description="Показать список вакансий"),
    ]
    await bot.set_my_commands(commands)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()  # Инициализируем диспетчер без параметров
    handlers = Handlers(bot)
    handlers.register(dp)

    await set_commands(bot)
    await dp.start_polling(bot)  # Запускаем поллинг с параметром bot


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    asyncio.run(main())  # Запускаем main в асинхронном режиме
