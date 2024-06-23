from aiogram import Router, types
from aiogram.filters import Command
from job_parser import get_vacancies, URL
from keyboards import Keyboards

class Handlers:
    def __init__(self, bot):
        self.bot = bot
        self.router = Router()

    def register(self, dp):
        dp.include_router(self.router)
        self.router.message.register(self.start, Command(commands=["start"]))
        self.router.message.register(self.help, Command(commands=["help"]))
        self.router.message.register(self.vacancies, Command(commands=["vacancies"]))
        self.router.message.register(self.echo)
        self.router.callback_query.register(self.process_callback, lambda c: c.data in ["today", "week", "all_time"])
        self.router.callback_query.register(self.process_site_callback, lambda c: c.data in ["hh", "proglib", "tproger", "habr", "all_sites"])
        self.router.callback_query.register(self.back_to_start, lambda c: c.data == "back_to_start")
        self.router.callback_query.register(self.back_to_sites, lambda c: c.data == "back_to_sites")
        self.router.callback_query.register(self.process_start, lambda c: c.data == "start")
        self.router.callback_query.register(self.process_help, lambda c: c.data == "help")

    async def start(self, message: types.Message):
        await message.reply(
            "Привет, для начала выбери кнопку",
            reply_markup=Keyboards.start_and_help_buttons(),
        )

    async def help(self, message: types.Message):
        await message.reply(
            "/start - начало работы\n"
            "/vacancies - показать список вакансий\n"
            "Пока больше ничего нет:("
        )

    async def vacancies(self, message: types.Message):
        await message.reply("Вакансии", reply_markup=Keyboards.vacancies_buttons())
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

    async def echo(self, message: types.Message):
        await message.reply("Я пока думаю как на такое отвечать")

    async def process_callback(self, callback_query: types.CallbackQuery):
        data = callback_query.data
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=f"Вы выбрали фильтр: {data}",
            reply_markup=None
        )
        await self.bot.answer_callback_query(callback_query.id)

    async def process_site_callback(self, callback_query: types.CallbackQuery):
        data = callback_query.data
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=f"Вы выбрали сайт: {data}\nТеперь выберите фильтр:",
            reply_markup=Keyboards.vacancies_buttons()
        )
        await self.bot.answer_callback_query(callback_query.id)

    async def back_to_start(self, callback_query: types.CallbackQuery):
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Привет, для начала выбери кнопку",
            reply_markup=Keyboards.start_and_help_buttons()
        )
        await self.bot.answer_callback_query(callback_query.id)

    async def back_to_sites(self, callback_query: types.CallbackQuery):
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Для начала выбери сайт",
            reply_markup=Keyboards.site_buttons()
        )
        await self.bot.answer_callback_query(callback_query.id)

    async def process_start(self, callback_query: types.CallbackQuery):
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Для начала выбери сайт",
            reply_markup=Keyboards.site_buttons()
        )
        await self.bot.answer_callback_query(callback_query.id)

    async def process_help(self, callback_query: types.CallbackQuery):
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=(
                "/start - начало работы\n"
                "/vacancies - показать список вакансий\n"
                "Пока больше ничего нет:("
            ),
            reply_markup=Keyboards.create_inline_keyboard([("Назад", "back_to_start")])
        )
        await self.bot.answer_callback_query(callback_query.id)

def register_handlers(dp, bot):
    handlers = Handlers(bot)
    handlers.register(dp)
