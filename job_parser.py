import requests
from bs4 import BeautifulSoup

URL = "https://hh.ru/?hhtmFrom=settings"


def get_html(url):
    response = requests.get(url)
    return response.text


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    vacancies = soup.find_all()

    for item in soup.find_all("div", class_="vacancy-serp-item"):
        title = item.find("a", class_="serp-item__title").text
        link = item.find("a", class_="serp-item__title").get["href"]
        salary = item.find("span", class_="bloco-header-selection-3").text
        if salary:
            salary = salary.text
        else:
            salary = "Не указано"
        description = item.find("div", class_="g-user-content").text
        vacancies.append(
            {"title": title, "link": link, "salary": salary, "description": description}
        )
    return vacancies


def get_vacancies(url):
    html = get_html(url)
    vacancies = parse_html(html)
    return vacancies
