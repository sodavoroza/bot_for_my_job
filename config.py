import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = "postgresql://postgres:13130422789099Vl@localhost/job_vacancies"
