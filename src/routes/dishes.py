from fastapi import HTTPException, APIRouter, status
from uuid import UUID

from src.database import actions
from src.models import schemas
from src.services import dish_service

router = APIRouter(prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dishes'])


@router.post('/', response_model=schemas.Dish, status_code=status.HTTP_201_CREATED)
async def create_dish(menu_id: UUID, submenu_id: UUID, dish: schemas.DishCreate):
    if not await actions.submenu_orm.check_exist(submenu_id=submenu_id, menu_id=menu_id):
        raise HTTPException(detail='submenu for not found', status_code=404)
    return await dish_service.create(data=dish, menu_id=menu_id, submenu_id=submenu_id)


@router.get('/', response_model=list[schemas.Dish])
async def get_dishes(menu_id: UUID, submenu_id: UUID, skip: int = 0, limit: int = 100):
    return await dish_service.get_list(menu_id=menu_id, submenu_id=submenu_id, skip=skip, limit=limit)


@router.get('/{dish_id}', response_model=schemas.Dish)
async def get_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    return await dish_service.get(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


@router.patch('/{dish_id}', response_model=schemas.Dish)
async def update_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dish: schemas.DishUpdate):
    return await dish_service.update(data=dish, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


@router.delete('/{dish_id}', response_model=schemas.Remove)
async def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    await dish_service.remove(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    return {'status': True, 'message': 'The dish has been deleted'}
