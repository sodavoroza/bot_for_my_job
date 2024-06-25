from aiogram import Bot
from aiogram.types import BotCommand

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу"),
        BotCommand(command="/help", description="Служба поддержки"),
        BotCommand(command="/vacancies", description="Показать вакансии")
    ]
    await bot.set_my_commands(commands)