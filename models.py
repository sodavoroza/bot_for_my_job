from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    site = Column(String, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    salary = Column(String)
    skills = Column(Text)
    link = Column(String)


Base.metadata.create_all(bind=engine)
