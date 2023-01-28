from fastapi import APIRouter, status
from uuid import UUID

from src.models import schemas
from src.services import menu_service

router = APIRouter(prefix='/menus', tags=["Menus"])


@router.post("/", response_model=schemas.Menu, status_code=status.HTTP_201_CREATED)
async def create_menu(menu: schemas.MenuCreate):
    return await menu_service.create(data=menu)


@router.get("/", response_model=list[schemas.Menu])
async def get_menus(skip: int = 0, limit: int = 100):
    return await menu_service.get_list(skip=skip, limit=limit)


@router.get("/{menu_id}", response_model=schemas.Menu)
async def get_menu(menu_id: UUID):
    return await menu_service.get(menu_id=menu_id)


@router.patch("/{menu_id}", response_model=schemas.Menu)
async def update_menu(menu_id: UUID, menu: schemas.MenuUpdate):
    return await menu_service.update(menu_id=menu_id, data=menu)


@router.delete("/{menu_id}", response_model=schemas.Remove)
async def delete_menu(menu_id: UUID):
    return {'status': await menu_service.remove(menu_id=menu_id),
            'message': 'The menu has been deleted'}
