import asyncio
from aiogram import Bot, Dispatcher
from handlers import Handlers
from config import DATABASE_URL
from models import Base, engine

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    handlers = Handlers(bot)
    handlers.register(dp)

    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    asyncio.run(main())
