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
    bot = Bot(token=BOT_TOKEN)  # Используем BOT_TOKEN из config
    dp = Dispatcher()
    handlers = Handlers(bot)
    handlers.register(dp)

    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    asyncio.run(main())
