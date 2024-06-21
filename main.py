import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router
from job_parser import get_vacancies, URL
from config import BOT_TOKEN


# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание объектов бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

start_and_help_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Перейти к вакансиям", callback_data="start"),
            InlineKeyboardButton(text="Нужна помощь?", callback_data="help"),
        ],
    ]
)


# Кнопки для фильтра вакансий
vacancies_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="За сегодня", callback_data="today"),
            InlineKeyboardButton(text="За неделю", callback_data="week"),
        ],
        [
            InlineKeyboardButton(text="Всё время", callback_data="all_time"),
        ],
    ]
)

# Добавьте этот код после определения всех InlineKeyboardMarkup
help_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back"),
        ]
    ]
)

command_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="/start", callback_data="start"),
            InlineKeyboardButton(text="/help", callback_data="help"),
            InlineKeyboardButton(text="/vacancies", callback_data="vacancies"),
        ]
    ]
)

# Добавьте этот хэндлер сразу после хэндлера process_callback
@router.callback_query(lambda c: c.data == "start")
async def process_start_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выберите фильтр вакансий", reply_markup=vacancies_buttons)
    await bot.answer_callback_query(callback_query.id)

# Добавьте этот хэндлер сразу после предыдущего
@router.callback_query(lambda c: c.data == "help")
async def process_help_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           "/start - начало работы\n"
                           "/vacancies - показать список вакансий"                           ,
                           reply_markup=help_buttons)
    await bot.answer_callback_query(callback_query.id)

# Добавьте этот хэндлер сразу после предыдущего
@router.callback_query(lambda c: c.data == "back")
async def process_back_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Привет, для начала выбери кнопку", reply_markup=start_and_help_buttons)
    await bot.answer_callback_query(callback_query.id)

# Добавьте этот хэндлер сразу после предыдущего
@router.message(Command(commands=["commands"]))
async def commands(message: types.Message):
    await message.reply("Доступные команды", reply_markup=command_buttons)

# Хэндлер команды /start
@router.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.reply(
        "Привет, для начала выбери кнопку",
        reply_markup=start_and_help_buttons,
    )


# Хэндлер команды /help
@router.message(Command(commands=["help"]))
async def help(message: types.Message):
    await message.reply(
        "/start - начало работы\n"
        "/vacancies - показать список вакансий"
    )
    await message.answer(start_and_help_buttons)


# Хэндлер команды /vacancies
@router.message(Command(commands=["vacancies"]))
async def vacancies(message: types.Message):
    await message.reply("Вакансии", reply_markup=vacancies_buttons)
    vacancies = get_vacancies(URL)  # Передача URL для парсинга
    if not vacancies:
        await message.reply("Вакансий за сегодня не найдено")
        return

    for vacancy in vacancies[:5]:
        reply = (
            f"Название: {vacancy['title']}\n"
            f"Описание: {vacancy['description']}\n"
            f"Зарплата: {vacancy['salary']}\n"
            f"Ссылка: {vacancy['link']}\n"
        )
        await message.answer(reply)


# Хэндлер для всех остальных сообщений
@router.message()
async def echo(message: types.Message):
    await message.reply("Я пока думаю как на такое отвечать")


# Хэндлер для обработки нажатий на кнопки
@router.callback_query(lambda c: c.data in ["today", "week", "all_time"])
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    await bot.send_message(callback_query.from_user.id, f"Вы выбрали фильтр: {data}")
    await bot.answer_callback_query(callback_query.id)


# Запуск поллинга
if __name__ == "__main__":
    dp.run_polling(bot, skip_updates=True)
