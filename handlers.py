from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from job_parser import get_vacancies, URL
from keyboards import start_and_help_buttons, site_buttons, vacancies_buttons, vacancy_buttons

router = Router()

@router.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.reply(
        "Привет, для начала выбери кнопку",
        reply_markup=start_and_help_buttons,
    )

@router.message(Command(commands=["help"]))
async def help(message: types.Message):
    await message.reply(
        "/start - начало работы\n"
        "/vacancies - показать список вакансий\n"
        "Пока больше ничего нет:("
    )
    await message.answer(reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_start")],
        ]
    ))

@router.message(Command(commands=["vacancies"]))
async def vacancies(message: types.Message):
    await message.reply("Вакансии", reply_markup=vacancies_buttons)
    vacancies = get_vacancies(URL)
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

@router.message()
async def echo(message: types.Message):
    await message.reply("Я пока думаю как на такое отвечать")

@router.callback_query(lambda c: c.data in ["today", "week", "all_time"])
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    await callback_query.message.edit_text(
        f"Вы выбрали фильтр: {data}"
    )
    await callback_query.answer()

@router.callback_query(lambda c: c.data in ["hh", "proglib", "tproger", "habr", "all_sites"])
async def process_site_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    await callback_query.message.edit_text(
        f"Вы выбрали сайт: {data}\nТеперь выберите фильтр:",
        reply_markup=vacancies_buttons
    )
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "back_to_start")
async def back_to_start(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Привет, для начала выбери кнопку",
        reply_markup=start_and_help_buttons
    )
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "back_to_sites")
async def back_to_sites(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Для начала выбери сайт",
        reply_markup=site_buttons
    )
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "start")
async def process_start(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Для начала выбери сайт",
        reply_markup=site_buttons
    )
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "help")
async def process_help(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "/start - начало работы\n"
        "/vacancies - показать список вакансий\n"
        "Пока больше ничего нет:(",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="back_to_start")],
            ]
        )
    )
    await callback_query.answer()