from aiogram import Router, types
import aiogram
from aiogram.filters import Command
from job_parser import JobParser
from keyboards import Keyboards

parser = JobParser()


class Handlers:
    def __init__(self, bot):
        self.bot = bot
        self.router = Router()
        self.parser = JobParser()
        self.parser.collect_vacancies()

    def register(self, dp):
        dp.include_router(self.router)
        self.router.message.register(self.start, Command(commands=["start"]))
        self.router.message.register(self.help, Command(commands=["help"]))
        self.router.message.register(self.vacancies, Command(commands=["vacancies"]))
        self.router.message.register(self.echo)
        self.router.callback_query.register(
            self.process_callback, lambda c: c.data in ["today", "week", "all_time"]
        )
        self.router.callback_query.register(
            self.process_site_callback,
            lambda c: c.data in ["hh", "proglib", "tproger", "habr", "all_sites"],
        )
        self.router.callback_query.register(
            self.back_to_start, lambda c: c.data == "back_to_start"
        )
        self.router.callback_query.register(
            self.back_to_sites, lambda c: c.data == "back_to_sites"
        )
        self.router.callback_query.register(
            self.process_start, lambda c: c.data == "start"
        )
        self.router.callback_query.register(
            self.process_help, lambda c: c.data == "help"
        )
        self.router.callback_query.register(
            self.process_vacancies, lambda c: c.data in ["detailed", "brief"]
        )
        self.router.callback_query.register(
            self.back_to_vacancies, lambda c: c.data == "back_to_vacancies"
        )

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

    async def echo(self, message: types.Message):
        await message.reply("Я пока думаю как на такое отвечать")

    async def process_callback(self, callback_query: types.CallbackQuery):
        data = callback_query.data
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=f"Вы выбрали фильтр: {data}",
            reply_markup=Keyboards.details_buttons(),
        )
        await self.bot.answer_callback_query(callback_query.id)

    async def process_site_callback(self, callback_query: types.CallbackQuery):
        data = callback_query.data
        vacancies_dict = self.parser.show_all_vacancies()

        if not vacancies_dict:
            await self.bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text="Ошибка при получении вакансий. Попробуйте снова.",
                reply_markup=Keyboards.site_buttons(),
            )
            await self.bot.answer_callback_query(callback_query.id)
            return

        vacancies = vacancies_dict.get(data, [])

        if not vacancies:
            await self.bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text="На выбранном сайте вакансий не найдено.",
                reply_markup=Keyboards.site_buttons(),
            )
            await self.bot.answer_callback_query(callback_query.id)
            return

        try:
            await self.bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=f"Вы выбрали сайт: {data}\nТеперь выберите фильтр:",
                reply_markup=Keyboards.vacancies_buttons(),
            )
        except aiogram.exceptions.TelegramBadRequest as e:
            if "message is not modified" in str(e):
                # Игнорируем исключение, если сообщение не изменилось
                pass
            else:
                # Если ошибка другая, выводим в лог или обрабатываем по-другому
                raise

        await self.bot.answer_callback_query(callback_query.id)

    async def back_to_start(self, callback_query: types.CallbackQuery):
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Привет, для начала выбери кнопку",
            reply_markup=Keyboards.start_and_help_buttons(),
        )
        await self.bot.answer_callback_query(callback_query.id)

    async def back_to_sites(self, callback_query: types.CallbackQuery):
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Теперь выбери сайт",
            reply_markup=Keyboards.site_buttons(),
        )
        await self.bot.answer_callback_query(callback_query.id)

    async def process_start(self, callback_query: types.CallbackQuery):
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Для начала выбери сайт",
            reply_markup=Keyboards.site_buttons(),
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
            reply_markup=Keyboards.create_inline_keyboard([("Назад", "back_to_start")]),
        )
        await self.bot.answer_callback_query(callback_query.id)

    async def process_vacancies(self, callback_query: types.CallbackQuery):
        data = callback_query.data
        detailed = data == "detailed"

        lines = callback_query.message.text.split("\n")

        # Проверяем, что есть хотя бы две строки в тексте сообщения
        if len(lines) < 2 or "Site:" not in lines[1]:
            await self.bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text="Ошибка: Неверный формат сообщения. Попробуйте снова.",
                reply_markup=Keyboards.create_inline_keyboard(
                    [("Назад", "back_to_vacancies")]
                ),
            )
            await self.bot.answer_callback_query(callback_query.id)
            return

        site = lines[1].split(":")[1].strip()

        # Получаем данные с сайта
        vacancies = parser.get_all_vacancies().get(site, [])

        if not vacancies:
            await self.bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text="Вакансий почему-то нет",
                reply_markup=Keyboards.create_inline_keyboard(
                    [("Назад", "back_to_vacancies")]
                ),
            )
            await self.bot.answer_callback_query(callback_query.id)
            return

        # Отправляем вакансии пользователю
        for vacancy in vacancies:
            if detailed:
                await self.bot.send_message(
                    chat_id=callback_query.message.chat.id,
                    text=f"{vacancy['title']}\n\n{vacancy['description']}\n\nЗарплата: {vacancy['salary']}\n\nСсылка: {vacancy['link']}",
                )
            else:
                await self.bot.send_message(
                    chat_id=callback_query.message.chat.id,
                    text=f"{vacancy['title']}\nЗарплата: {vacancy['salary']}\nСсылка: {vacancy['link']}",
                )

        await self.bot.answer_callback_query(callback_query.id)

    async def back_to_vacancies(self, callback_query: types.CallbackQuery):
        await self.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Вакансии",
            reply_markup=Keyboards.vacancies_buttons(),
        )
        await self.bot.answer_callback_query(callback_query.id)
