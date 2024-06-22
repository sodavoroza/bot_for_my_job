import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import BOT_TOKEN
from handlers import router
from commands import set_commands

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание объектов бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)

async def main():
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
