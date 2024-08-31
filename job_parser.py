from hh_pars import extract_titles as extract_hh_titles
from habr_pars import extract_vacancies as extract_habr_vacancies
from tproger_pars import extract_vacancies as extract_tproger_vacancies


class JobParser:
    def __init__(self):
        self.vacancies = {
            "hh": [],
            "habr": [],
            "tproger": [],
            "proglib": [],
        }

    def collect_vacancies(self):
        # Получаем вакансии с hh.ru
        print("Парсинг hh.ru...")
        hh_vacancies = extract_hh_titles(
            "https://hh.ru/search/vacancy?st=searchVacancy&text=Python+программист&items_on_page=100"
        )
        self.vacancies["hh"] = hh_vacancies

        # Получаем вакансии с Habr Career
        print("Парсинг Habr Career...")
        habr_vacancies = extract_habr_vacancies(
            "https://career.habr.com/vacancies?type=all"
        )
        self.vacancies["habr"] = habr_vacancies

        # Получаем вакансии с Tproger
        print("Парсинг Tproger...")
        tproger_vacancies = extract_tproger_vacancies("https://tproger.ru/jobs")
        self.vacancies["tproger"] = tproger_vacancies

    def show_all_vacancies(self):
        return self.vacancies


if __name__ == "__main__":
    parser = JobParser()
    parser.collect_vacancies()
