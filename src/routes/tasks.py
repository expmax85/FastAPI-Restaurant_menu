from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import FileResponse

from celery.result import AsyncResult
from src.celery.celery_app import import_all_menus
from src.database.actions import MenuAction, get_menu_orm
from src.database.init_data_db import init_test_data_db
from src.models import schemas

router = APIRouter()


@router.post(
    "/tasks/import",
    response_model=schemas.CreateTask,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Tasks"],
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
    "/tasks/status/{task_id}",
    response_class=FileResponse,
    responses={
        202: {
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
            },
            "description": "Return the xlsx file.",
        },
        400: {"model": schemas.TaskStatus, "description": "File not found"},
    },
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Tasks"],
)
async def get_task_status(task_id: str):
    """
    Get file by task_id. If it's not complete, returned the dict with task status
    """
    task_result = AsyncResult(task_id)
    task_result.ready()
    if task_result.status == "SUCCESS":
        filename = task_result.result.split("/")[-1]
        return FileResponse(
            path=task_result.result,
            media_type="application/octet-stream",
            filename=filename,
        )
    return {
        "task_id": task_id,
        "status": task_result.status,
    }


@router.get(
    "/generate",
    response_model=schemas.SuccessInit,
    status_code=status.HTTP_200_OK,
    tags=["Generate data"],
)
async def generate_test_data():
    """
    Service route for generating test menus, submenus and dishes data
    """
    try:
        await init_test_data_db()
    except Exception:
        raise HTTPException(
            detail="Wrong data", status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    return {"status": True, "message": "All data was created"}
