from celery import Celery
from src.celery.import_service import ImportXLS
from src.config import settings
from src.services.base_servises import AbstractImportClass

celery_app = Celery(__name__)
celery_app.conf.broker_url = settings.CELERY_BROKER_URL
celery_app.conf.result_backend = settings.CELERY_BACKEND_URL


@celery_app.task(name="import_all_menus")
def import_all_menus(data: list[dict], filename: str) -> dict:
    task: AbstractImportClass = ImportXLS(filename=filename)
    result = task.make_import(data)
    return result
