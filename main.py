import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram import Router
from dotenv import load_dotenv  # Импортируем библиотеку dotenv
from job_parser import get_vacancies, URL

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверка наличия токена
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание объектов бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


# Установка команд, которые будут отображаться в меню
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу"),
        BotCommand(command="/help", description="Служба поддержки"),
        BotCommand(command="/vacancies", description="Показать вакансии"),
    ]
    await bot.set_my_commands(commands)


# Кнопки для начала и помощи
start_and_help_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Перейти к вакансиям", callback_data="start"),
            InlineKeyboardButton(text="Нужна помощь?", callback_data="help"),
        ],
    ]
)

# Кнопки для выбора сайта
site_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="hh.ru", callback_data="hh"),
            InlineKeyboardButton(text="proglib.io", callback_data="proglib"),
            InlineKeyboardButton(text="tproger.ru", callback_data="tproger"),
            InlineKeyboardButton(text="career.habr.com", callback_data="habr"),
        ],
        [
            InlineKeyboardButton(text="Все сразу", callback_data="all_sites"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back_to_start"),
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
            InlineKeyboardButton(text="Назад", callback_data="back_to_sites"),
        ],
    ]
)


# Хэндлер команды /start с новым меню выбора сайта
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
        "/vacancies - показать список вакансий\n"
        "Пока больше ничего нет:("
    )
    await message.answer(
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="back_to_start")],
            ]
        )
    )


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


# Хэндлер для обработки нажатий на кнопки фильтра вакансий
@router.callback_query(lambda c: c.data in ["today", "week", "all_time"])
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=f"Вы выбрали фильтр: {data}",
        reply_markup=None,
    )
    await bot.answer_callback_query(callback_query.id)


# Хэндлер для обработки нажатий на кнопки выбора сайта
@router.callback_query(
    lambda c: c.data in ["hh", "proglib", "tproger", "habr", "all_sites"]
)
async def process_site_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=f"Вы выбрали сайт: {data}\nТеперь выберите фильтр:",
        reply_markup=vacancies_buttons,
    )
    await bot.answer_callback_query(callback_query.id)


# Хэндлер для кнопки "Назад" в меню выбора сайта
@router.callback_query(lambda c: c.data == "back_to_start")
async def back_to_start(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Привет, для начала выбери кнопку",
        reply_markup=start_and_help_buttons,
    )
    await bot.answer_callback_query(callback_query.id)


# Хэндлер для кнопки "Назад" в меню фильтра вакансий
@router.callback_query(lambda c: c.data == "back_to_sites")
async def back_to_sites(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Для начала выбери сайт",
        reply_markup=site_buttons,
    )
    await bot.answer_callback_query(callback_query.id)


# Хэндлер для обработки нажатий на кнопки "Перейти к вакансиям"
@router.callback_query(lambda c: c.data == "start")
async def process_start(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Для начала выбери сайт",
        reply_markup=site_buttons,
    )
    await bot.answer_callback_query(callback_query.id)


# Хэндлер для обработки нажатий на кнопку "Нужна помощь?"
@router.callback_query(lambda c: c.data == "help")
async def process_help(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=(
            "/start - начало работы\n"
            "/vacancies - показать список вакансий\n"
            "Пока больше ничего нет:("
        ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="back_to_start")],
            ]
        ),
    )
    await bot.answer_callback_query(callback_query.id)


# Запуск поллинга
if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_commands(bot))
    dp.run_polling(bot, skip_updates=True)
