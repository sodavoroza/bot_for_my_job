from sqlalchemy.orm import Session
from models import Vacancy, SessionLocal


class VacancyManager:
    def __init__(self):
        self.db = SessionLocal()

    def add_vacancies(self, site, vacancies):
        for vacancy in vacancies:
            db_vacancy = Vacancy(
                site=site,
                title=vacancy["title"],
                description=vacancy["description"],
                salary=vacancy["salary"],
                skills=vacancy.get("skills", ""),
                link=vacancy["link"],
            )
            self.db.add(db_vacancy)
        self.db.commit()

    def get_vacancies(self, site):
        return self.db.query(Vacancy).filter(Vacancy.site == site).all()

    def clear(self):
        self.db.query(Vacancy).delete()
        self.db.commit()

    def close(self):
        self.db.close()
