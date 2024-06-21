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

# Кнопки для фильтра вакансий
start_buttons = InlineKeyboardMarkup(
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


# Хэндлер команды /start
@router.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.reply(
        "Привет, для начала поиска сегодняшних вакансий нажми на кнопку",
        reply_markup=start_buttons,
    )


# Хэндлер команды /vacancies
@router.message(Command(commands=["vacancies"]))
async def vacancies(message: types.Message):
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


# Хэндлер команды /help
@router.message(Command(commands=["help"]))
async def help(message: types.Message):
    help_text = (
        "/start - начало работы\n"
        "/vacancies - показать список вакансий\n"
        "/help - показать это сообщение"
    )
    await message.answer(help_text)


# Запуск поллинга
if __name__ == "__main__":
    dp.run_polling(bot, skip_updates=True)
