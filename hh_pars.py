import requests
from bs4 import BeautifulSoup

URL = "https://hh.ru/search/vacancy?st=searchVacancy&text=Python+программист&items_on_page=100"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def extract_titles(url):
    result = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(result.text, "html.parser")

    # Поиск всех вакансий на странице
    vacancies = soup.find_all("div", {"class": "magritte-card___bhGKz_6-0-12"})

    for vacancy in vacancies:
        # Извлечение названия вакансии
        title_elem = vacancy.find("a", class_="magritte-link___b4rEM_4-2-6")
        title = title_elem.get_text(strip=True) if title_elem else "Не указано"

        # Извлечение ссылки на вакансию
        link = title_elem["href"] if title_elem else "Не указана"

        # Извлечение зарплаты и опыта, если указано
        salary_elem = vacancy.find(
            "div", class_="compensation-labels--uUto71l5gcnhU2I8TZmz"
        )
        salary = salary_elem.get_text(strip=True) if salary_elem else "Не указана"

        # Извлечение информации о метро, если указана
        metro_elem = vacancy.find("span", class_="metro-station")
        metro_info = metro_elem.get_text(strip=True) if metro_elem else "Не указано"

        print(f"Название вакансии: {title}")
        print(f"Ссылка: {link}")
        print(f"Зарплата и опыт: {salary}")
        print(f"Метро: {metro_info}")
        print("-" * 40)


if __name__ == "__main__":
    extract_titles(URL)
