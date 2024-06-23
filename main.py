import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import register_handlers

class BotApp:
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()

    async def set_commands(self):
        commands = [
            BotCommand(command="/start", description="Начать работу"),
            BotCommand(command="/help", description="Служба поддержки"),
            BotCommand(command="/vacancies", description="Показать вакансии"),
        ]
        await self.bot.set_my_commands(commands)

    def register_handlers(self):
        register_handlers(self.dp, self.bot)

    async def run(self):
        await self.set_commands()
        self.register_handlers()
        await self.dp.start_polling(self.bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = BotApp(BOT_TOKEN)
    asyncio.run(app.run())
