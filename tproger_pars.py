import requests
from bs4 import BeautifulSoup

URL = "https://tproger.ru/jobs"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def extract_vacancies(url):
    result = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(result.text, "html.parser")

    # Поиск всех блоков с вакансиями на странице
    vacancies = soup.find_all(
        "div", class_="tp-feed__item tp-feed__item--entity tp-feed-item-job"
    )

    for vacancy in vacancies:
        # Извлечение заголовка вакансии
        title_tag = vacancy.find("h1", class_="tp-ui-job-card__title")
        title = title_tag.text.strip() if title_tag else "Title not found"

        # Извлечение адреса вакансии
        link_tag = title_tag.find("a") if title_tag else None
        link = link_tag.get("href") if link_tag else "Link not found"
        full_link = f"https://tproger.ru{link}" if link != "Link not found" else link

        # Извлечение уровня позиции
        position_level_chip = vacancy.find_all("span", class_="tp-ui-chip")
        position_levels = [
            chip.text.strip()
            for chip in position_level_chip
            if "По итогам собеседования" not in chip.text
        ]
        position_level = (
            ", ".join(position_levels)
            if position_levels
            else "Position level not found"
        )

        # Вывод информации о вакансии
        print(f"Job Title: {title}")
        print(f"Job Link: {full_link}")
        print(f"Position Level: {position_level}")
        print("-" * 40)


if __name__ == "__main__":
    extract_vacancies(URL)
