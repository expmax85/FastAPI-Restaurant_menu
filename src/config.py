import os

from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    load_dotenv('.env')
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")


settings = Settings()
