import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(
        "Привет, для старта поиска сегодняшних вакансий нажми на кнопку"
    )


@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(message.text)
