import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).parent.parent
FIXTURES_DIR = os.path.join(BASE_DIR, 'fixtures')

if os.getenv("CONFIG_FILE") and os.path.exists(
    os.path.join(BASE_DIR, os.getenv("CONFIG_FILE", ".env.default"))
):
    env_path = os.path.join(BASE_DIR, os.getenv("CONFIG_FILE", ".env.default"))
else:
    env_path = os.path.join(BASE_DIR, "conf", os.getenv("CONFIG_FILE", ".env.default"))


class App(BaseSettings):
    DEBUG: bool = False
    TITLE: str = "FastAPI"
    DESCRIPTION: str = ""
    PREFIX: str = "/api/v1"
    VERSION: str = "1.0"
    MENU_CACHE_KEY: str = "all_menus"
    SUBMENU_CACHE_KEY: str = "all_submenus"
    DISH_CACHE_KEY: str = "all_dishes"

    class Config:
        env_file = env_path


class DBconfig(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int

    class Config:
        env_file: str = env_path


class Redisconfig(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file: str = env_path


class RabbitMQ(BaseSettings):
    RABBIT_HOST: str
    RABBIT_PORT: int
    RABBIT_USER: str = "guest"
    RABBIT_PASSWORD: str = "guest"

    class Config:
        env_file: str = env_path


class Settings(BaseSettings):
    App: App = App()
    Database: DBconfig = DBconfig()
    Redis: Redisconfig = Redisconfig()
    RabbitMQ: RabbitMQ = RabbitMQ()

    DATABASE_URL: str = (
        f"postgresql+asyncpg://{Database.DB_USER}:{Database.DB_PASSWORD}"
        f"@{Database.DB_HOST}/{Database.DB_NAME}"
    )
    CACHE_URL: str = f"redis://{Redis.REDIS_HOST}"
    CELERY_BROKER_URL: str = f"amqp://{RabbitMQ.RABBIT_USER}:{RabbitMQ.RABBIT_PASSWORD}@{RabbitMQ.RABBIT_HOST}/"
    CELERY_BACKEND_URL: str = f"rpc://{Redis.REDIS_HOST}"


settings = Settings()
