import requests
from bs4 import BeautifulSoup
import time
import random

URLS = {
    "hh": "https://hh.ru/search/vacancy?st=searchVacancy&text=Python+программист&items_on_page=100",
    "proglib": "https://proglib.io/vacancies/all",
    "tproger": "https://tproger.ru/jobs",
    "habr": "https://career.habr.com/vacancies?type=all",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


class JobParser:
    def __init__(self):
        self.urls = URLS
        self.headers = HEADERS

    def get_html(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Проверка статуса ответа
            time.sleep(
                random.uniform(2, 5)
            )  # Задержка между запросами от 2 до 5 секунд
            return response.text
        except requests.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return ""

    def parse_hh(self, html):
        soup = BeautifulSoup(html, "html.parser")
        vacancies = []

        for item in soup.find_all("div", class_="vacancy-search-item__card serp-item_link vacancy-card-container--OwxCdOj5QlSlCBZvSggS"):
            title_tag = item.find("a", class_="bloko-link")
            title = title_tag.text if title_tag else "Не указано"
            link = title_tag["href"] if title_tag else "Не указано"
            salary_tag = item.find("div", class_="compensation-labels--uUto71l5gcnhU2I8TZmz")
            salary = salary_tag.text if salary_tag else "Не указана"
            metro_tag = item.find("span", class_="metro-station")
            metro = metro_tag.text if metro_tag else "Не указано"

            vacancies.append(
                {
                    "title": title,
                    "link": link,
                    "salary": salary,
                    "description": metro,
                }
            )
        return vacancies

    def get_hh_vacancies(self, url):
        html = self.get_html(url)
        if html:
            return self.parse_hh(html)
        return []

    def get_all_vacancies(self):
        all_vacancies = {}
        for site, url in self.urls.items():
            if site == "hh":
                vacancies = self.get_hh_vacancies(url)
                all_vacancies[site] = vacancies
        return all_vacancies


if __name__ == "__main__":
    parser = JobParser()
    vacancies = parser.get_all_vacancies()
    for site, jobs in vacancies.items():
        print(f"\nSite: {site}")
        for job in jobs:
            print(
                f"Title: {job['title']}, Link: {job['link']}, Salary: {job['salary']}, Description: {job['description']}"
            )
