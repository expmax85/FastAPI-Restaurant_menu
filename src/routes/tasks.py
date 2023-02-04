from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from src.celery.celery_app import import_all_menus
from src.database.actions import MenuAction, get_menu_orm
from src.database.init_data_db import init_test_data_db

router = APIRouter(tags=["Tasks"])


@router.get('/init_menus')
async def init_db():
    await init_test_data_db()
    return {'status': True, 'message': 'All data was created'}


@router.post("/test_celery")
async def test_celery(filename: str, menu_serv: MenuAction = Depends(get_menu_orm)):
    data = await menu_serv.get_all_data()
    task = import_all_menus.delay(data=jsonable_encoder(data), filename=filename)
    return {"task_id": task.id}
