import requests
from bs4 import BeautifulSoup
import time
import random

# URL для всех сайтов
URLS = {
    "hh": "https://hh.ru/search/vacancy?text=Python+developer&area=1",
    "proglib": "https://proglib.io/vacancies/all",
    "tproger": "https://tproger.ru/jobs",
    "habr": "https://career.habr.com/vacancies?type=all"
}

# Заголовки для авторизации
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Функция для получения HTML
def get_html(url):
    response = requests.get(url, headers=HEADERS)
    time.sleep(random.uniform(2, 5))  # Задержка между запросами от 2 до 5 секунд
    return response.text

# Функция для парсинга HTML hh.ru
def parse_hh(html):
    soup = BeautifulSoup(html, "html.parser")
    vacancies = []

    for item in soup.find_all("div", class_="vacancy-serp-item"):
        title = item.find("a", class_="serp-item__title").text
        link = item.find("a", class_="serp-item__title")["href"]
        salary_tag = item.find("span", class_="bloko-header-section-3")
        salary = salary_tag.text if salary_tag else "Не указана"
        description = item.find("div", class_="g-user-content").text
        vacancies.append({
            "title": title,
            "link": link,
            "salary": salary,
            "description": description
        })
    return vacancies

# Функция для получения вакансий с hh.ru
def get_hh_vacancies(url):
    html = get_html(url)
    return parse_hh(html)

# Функция для получения вакансий для всех сайтов
def get_all_vacancies():
    all_vacancies = {}
    for site, url in URLS.items():
        if site == "hh":
            vacancies = get_hh_vacancies(url)
        # Здесь добавим обработчики для других сайтов
        all_vacancies[site] = vacancies
    return all_vacancies

# Пример использования
if __name__ == "__main__":
    vacancies = get_all_vacancies()
    for site, vacancies in vacancies.items():
        print(f"Вакансии с {site}:")
        for vacancy in vacancies:
            print(vacancy)
