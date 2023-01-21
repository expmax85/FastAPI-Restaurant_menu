import os
from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent.parent / 'conf'
env_path = os.path.join(BASE_DIR, os.getenv('CONFIG_FILE', '.env.default'))


class Settings(BaseSettings):
    DEBUG: bool
    DB_NAME: str
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    TEST_DB_NAME: str

    class Config:
        env_file = env_path


settings = Settings()

_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}"
SQLALCHEMY_DATABASE_URL = "/".join([_DATABASE_URL, settings.DB_NAME])
TEST_DATABASE_URL = "/".join([_DATABASE_URL, settings.TEST_DB_NAME])
