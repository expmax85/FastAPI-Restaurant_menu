import os
from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent.parent / 'conf'
env_path = os.path.join(BASE_DIR, os.getenv('CONFIG_FILE', '.env.default'))


class App(BaseSettings):
    DEBUG: bool = False
    TITLE: str = 'FastAPI'
    DESCRIPTION: str = ''
    PREFIX: str = '/api/v1'
    VERSION: str = '1.0'
    MENU_CACHE_KEY: str = 'all_menus'
    SUBMENU_CACHE_KEY: str = 'all_submenus'
    DISH_CACHE_KEY: str = 'all_dishes'

    class Config:
        env_file = env_path


class DB_conf(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int

    class Config:
        env_file = env_path


class Redis_conf(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = env_path


class Settings(BaseSettings):
    App: App = App()
    Database: DB_conf = DB_conf()
    Redis_conf: Redis_conf = Redis_conf()
    DATABASE_URL: str = f'postgresql+asyncpg://{Database.DB_USER}:{Database.DB_PASSWORD}' \
                        f'@{Database.DB_HOST}/{Database.DB_NAME}'

    class Config:
        env_file = env_path


settings = Settings()
