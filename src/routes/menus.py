from fastapi import APIRouter, status, HTTPException
from uuid import UUID

from src.database import actions
from src.models import schemas
from src.services import menu_service

router = APIRouter(prefix='/menus', tags=["Menus"])


@router.post("/", response_model=schemas.Menu, status_code=status.HTTP_201_CREATED)
async def create_menu(menu: schemas.MenuCreate):
    return await actions.menu_orm.create(obj_in=menu)


@router.get("/", response_model=list[schemas.Menu])
async def get_menus(skip: int = 0, limit: int = 100):
    return await actions.menu_orm.get_all_with_relates(skip=skip, limit=limit)


@router.get("/{menu_id}", response_model=schemas.Menu)
async def get_menu(menu_id: UUID):
    if not (result := await menu_service.get_with_relates(menu_id=menu_id)):
        raise HTTPException(detail="menu not found", status_code=404)
    return result


@router.patch("/{menu_id}", response_model=schemas.Menu)
async def update_menu(menu_id: UUID, menu: schemas.MenuUpdate):
    if not await actions.menu_orm.check_exist(menu_id=menu_id):
        raise HTTPException(detail="menu not found", status_code=404)
    await actions.menu_orm.update(id_obj=menu_id, obj_data=menu)
    return await actions.menu_orm.get_with_relates(menu_id=menu_id)


@router.delete("/{menu_id}", response_model=schemas.Remove)
async def delete_menu(menu_id: UUID):
    if not await actions.menu_orm.check_exist(menu_id=menu_id):
        raise HTTPException(detail='menu not exists', status_code=404)
    return {'status': await actions.menu_orm.remove(id_obj=menu_id),
            'message': 'The menu has been deleted'}
