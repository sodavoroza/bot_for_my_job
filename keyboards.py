from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Keyboards:
    @staticmethod
    def create_inline_keyboard(buttons):
        keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=callback_data)] for text, callback_data in buttons])
        return keyboard

    @staticmethod
    def start_and_help_buttons():
        buttons = [
            ("Перейти к вакансиям", "start"),
            ("Нужна помощь?", "help")
        ]
        return Keyboards.create_inline_keyboard(buttons)

    @staticmethod
    def site_buttons():
        buttons = [
            ("hh.ru", "hh"),
            ("proglib.io", "proglib"),
            ("tproger.ru", "tproger"),
            ("habr.com", "habr"),
            ("Все сайты", "all_sites"),
            ("Назад", "back_to_start")
        ]
        return Keyboards.create_inline_keyboard(buttons)

    @staticmethod
    def vacancies_buttons():
        buttons = [
            ("За сегодня", "today"),
            ("За неделю", "week"),
            ("За всё время", "all_time"),
            ("Назад", "back_to_sites")
        ]
        return Keyboards.create_inline_keyboard(buttons)
