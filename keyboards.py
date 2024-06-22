from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_and_help_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Перейти к вакансиям", callback_data="start"),
            InlineKeyboardButton(text="Нужна помощь?", callback_data="help"),
        ],
    ]
)

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
