# vacancy_manager.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL

# Инициализация базы данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Определение модели вакансий
class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    link = Column(String)
    salary = Column(String)
    description = Column(String)
    site = Column(String)


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)


class VacancyManager:
    def __init__(self):
        self.session = SessionLocal()

    def add_vacancy(self, vacancy):
        db_vacancy = Vacancy(
            title=vacancy["title"],
            link=vacancy["link"],
            salary=vacancy["salary"],
            description=vacancy["description"],
            site=vacancy["site"],
        )
        self.session.add(db_vacancy)
        self.session.commit()

    def get_vacancies(self, site):
        return self.session.query(Vacancy).filter(Vacancy.site == site).all()

    def add_vacancies(self, site, vacancies):
        for vacancy in vacancies:
            vacancy["site"] = site
            self.add_vacancy(vacancy)
