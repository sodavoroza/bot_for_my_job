import requests
from bs4 import BeautifulSoup

URL = "https://hh.ru/search/vacancy?text=Python+developer&area=1"

def get_html(url):
    response = requests.get(url)
    return response.text

def parse_html(html):
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

def get_vacancies(url=URL):
    html = get_html(url)
    vacancies = parse_html(html)
    return vacancies
