import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram import Command
import json
from job_parser import get_vacancies
from config import BOT_TOKEN
import os
from dotenv import load_dotenv

with open("config.json") as f:
    config = json.load(f)

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(
        "Привет, для начала поиска сегодняшних вакансий нажми на кнопку"
    )


@dp.message_handler(commands=["vacancies"])
async def vacancies(message: types.Message):
    vacancies = get_vacancies()
    if not vacancies:
        await message.reply("Вкансий за сегодня не найдено")
        return
    
    for vacancy in vacancies[:5]:
        reply = (f"Название: {vacancy["title"]}\n"
                f"Описание: {vacancy['description']}\n"
                f"Зарплата: {vacancy['salary']}\n"
                f"Ссылка: {vacancy['link']}\n")
        await message.answer(reply)

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply("Я пока думаю как на такое отвечать")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

