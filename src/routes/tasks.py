from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status

from celery.result import AsyncResult
from src.celery.celery_app import import_all_menus
from src.database.actions import MenuAction, get_menu_orm
from src.models import schemas

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/import", response_model=schemas.CreateTask, status_code=status.HTTP_202_ACCEPTED
)
async def import_from_db_to_file(
    filename: str, menu_serv: MenuAction = Depends(get_menu_orm)
):
    """
    Route to creating the importing task
    """
    data = await menu_serv.get_all_data()
    task = import_all_menus.delay(data=jsonable_encoder(data), filename=filename)
    return {"task_id": task.id}


@router.get(
    "/status/{task_id}",
    response_model=schemas.TaskStatus,
    status_code=status.HTTP_200_OK,
)
async def get_task_status(task_id: str):
    """
    Get task status by task_id
    """
    task_result = AsyncResult(task_id)
    task_result.ready()
    return {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
