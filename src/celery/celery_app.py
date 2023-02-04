from celery import Celery
from src.celery.import_service import ImportXLS
from src.config import settings

celery_app = Celery(__name__)
celery_app.conf.broker_url = settings.BROKER_URL
# backend="amqp://guest:guest@web_rabbitmq/", #f"redis://{settings.Redis.REDIS_HOST}",
# broker="amqp://guest:guest@web_rabbitmq/"


@celery_app.task(name='import_all_menus')
def import_all_menus(data: list[dict], filename: str) -> dict:
    task = ImportXLS(filename=filename)
    result = task.make_import(data)
    return result
