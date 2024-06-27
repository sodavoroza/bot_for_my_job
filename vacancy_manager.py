import sqlite3


class VacancyManager:
    def __init__(self, db_name="vacancies.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                link TEXT,
                salary TEXT,
                description TEXT,
                site TEXT
            )
            """
        )
        self.conn.commit()

    def add_vacancy(self, vacancy):
        self.cursor.execute(
            """
            INSERT INTO vacancies (title, link, salary, description, site)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                vacancy["title"],
                vacancy["link"],
                vacancy["salary"],
                vacancy["description"],
                vacancy["site"],
            ),
        )
        self.conn.commit()

    def get_vacancies(self, site):
        self.cursor.execute(
            """
            SELECT title, link, salary, description
            FROM vacancies
            WHERE site = ?
            """,
            (site,),
        )
        rows = self.cursor.fetchall()
        return [
            {"title": row[0], "link": row[1], "salary": row[2], "description": row[3]}
            for row in rows
        ]

    def add_vacancies(self, site, vacancies):
        for vacancy in vacancies:
            vacancy["site"] = site
            self.add_vacancy(vacancy)


from aiogram.types import CallbackQuery


async def process_vacancies(callback_query: CallbackQuery):
    try:
        # Проверка, содержит ли текст сообщение как минимум две строки
        text_lines = callback_query.message.text.split("\n")
        if len(text_lines) < 2:
            raise ValueError("Message text does not contain enough lines")

        site_line = text_lines[1]
        # Проверка, содержит ли строка двоеточие для разделения
        if ":" not in site_line:
            raise ValueError("Site line does not contain ':'")

        site = site_line.split(":")[1].strip()
        # Дальнейшая обработка
        # ...

    except ValueError as ve:
        print(f"ValueError: {ve}")
        # Отправка сообщения пользователю о некорректном формате данных
        await callback_query.message.answer(
            "Некорректный формат данных. Пожалуйста, попробуйте снова."
        )

    except IndexError as ie:
        print(f"IndexError: {ie}")
        # Отправка сообщения пользователю о некорректном формате данных
        await callback_query.message.answer(
            "Произошла ошибка при обработке данных. Пожалуйста, попробуйте снова."
        )

    except Exception as e:
        print(f"Exception: {e}")
        # Обработка остальных исключений
        await callback_query.message.answer(
            "Произошла непредвиденная ошибка. Пожалуйста, попробуйте снова."
        )
