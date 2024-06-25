import requests
from bs4 import BeautifulSoup
import time
import random


URLS = {
    "hh": "https://hh.ru/search/vacancy?text=Python+developer&area=1",
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
        response = requests.get(url, headers=self.headers)
        time.sleep(random.uniform(2, 5))  # Задержка между запросами от 2 до 5 секунд
        return response.text

    def parse_hh(self, html):
        soup = BeautifulSoup(html, "html.parser")
        vacancies = []

        for item in soup.find_all("div", class_="vacancy-serp-item"):
            title = item.find("a", class_="serp-item__title").text
            link = item.find("a", class_="serp-item__title")["href"]
            salary_tag = item.find("span", class_="bloko-header-section-3")
            salary = salary_tag.text if salary_tag else "Не указана"
            description = item.find("div", class_="g-user-content").text
            vacancies.append(
                {
                    "title": title,
                    "link": link,
                    "salary": salary,
                    "description": description,
                }
            )
        return vacancies

    def get_hh_vacancies(self, url):
        html = self.get_html(url)
        return self.parse_hh(html)

    def get_all_vacancies(self):
        all_vacancies = {}
        for site, url in self.urls.items():
            if site == "hh":
                vacancies = self.get_hh_vacancies(url)

            all_vacancies[site] = vacancies
        return all_vacancies
