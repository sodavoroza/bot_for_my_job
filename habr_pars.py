import requests
from bs4 import BeautifulSoup

URL = "https://career.habr.com/vacancies?type=all"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def extract_vacancies(url):
    result = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(result.text, "html.parser")

    # Поиск всех блоков с вакансиями на странице
    vacancies = soup.find_all("div", class_="vacancy-card")

    for vacancy in vacancies:
        # Извлечение заголовка вакансии
        title_tag = vacancy.find("a", class_="vacancy-card__title-link")
        title = title_tag.text.strip() if title_tag else "Title not found"

        # Извлечение адреса вакансии
        link = title_tag.get("href") if title_tag else "Link not found"
        full_link = (
            f"https://career.habr.com{link}" if link != "Link not found" else link
        )

        # Извлечение зарплаты
        salary_div = vacancy.find("div", class_="vacancy-card__salary")
        salary = (
            salary_div.text.strip()
            if salary_div and salary_div.text.strip()
            else "Salary not specified"
        )

        # Извлечение уровня позиции
        skills_div = vacancy.find("div", class_="vacancy-card__skills")
        position_levels = (
            [
                skill.text.strip()
                for skill in skills_div.find_all("a")
                if "Средний" in skill.text
                or "Junior" in skill.text
                or "Senior" in skill.text
            ]
            if skills_div
            else []
        )
        position_level = (
            ", ".join(position_levels)
            if position_levels
            else "Position level not found"
        )

        # Вывод информации о вакансии
        print(f"Job Title: {title}")
        print(f"Job Link: {full_link}")
        print(f"Salary: {salary}")
        print(f"Position Level: {position_level}")
        print("-" * 40)


if __name__ == "__main__":
    extract_vacancies(URL)
