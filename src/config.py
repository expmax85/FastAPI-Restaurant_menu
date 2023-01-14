import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv('.env')
DATABASE_URL = os.getenv("DATABASE_URL")


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL = DATABASE_URL


settings = Settings()
