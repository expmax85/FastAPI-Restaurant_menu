from fastapi import HTTPException, APIRouter, status
from uuid import UUID

from src.database import actions
from src.models import schemas


router = APIRouter(prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=["Dishes"])


@router.post("/", response_model=schemas.Dish, status_code=status.HTTP_201_CREATED)
async def create_dish(menu_id: UUID, submenu_id: UUID, dish: schemas.DishCreate):
    if not await actions.submenu_orm.check_exist(submenu_id=submenu_id, menu_id=menu_id):
        raise HTTPException(detail="submenu for not found", status_code=404)
    return await actions.dish_orm.create(obj_in=dish, submenu_id=submenu_id)


@router.get("/", response_model=list[schemas.Dish])
async def get_dishes(menu_id: UUID, submenu_id: UUID, skip: int = 0, limit: int = 100):
    return await actions.dish_orm.get_all_with_relates(menu_id=menu_id, submenu_id=submenu_id,
                                                       skip=skip, limit=limit)


@router.get("/{dish_id}", response_model=schemas.Dish)
async def get_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    if not (result := await actions.dish_orm.get_with_relates(menu_id=menu_id, submenu_id=submenu_id,
                                                              dish_id=dish_id)):
        raise HTTPException(detail="dish not found", status_code=404)
    return result


@router.patch("/{dish_id}", response_model=schemas.Dish)
async def update_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dish: schemas.DishUpdate):
    exists_submenu = await actions.submenu_orm.check_exist(menu_id=menu_id, submenu_id=submenu_id)
    exists_dish = await actions.dish_orm.check_exist(dish_id=dish_id, submenu_id=submenu_id)
    if not exists_submenu and not exists_dish:
        raise HTTPException(detail="dish not found", status_code=404)
    return await actions.dish_orm.update(id_obj=dish_id, obj_data=dish)


@router.delete("/{dish_id}", response_model=schemas.Remove)
async def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    exists_submenu = await actions.submenu_orm.check_exist(menu_id=menu_id, submenu_id=submenu_id)
    exists_dish = await actions.dish_orm.check_exist(dish_id=dish_id, submenu_id=submenu_id)
    if not exists_submenu and not exists_dish:
        raise HTTPException(detail="dish not found", status_code=404)
    await actions.dish_orm.remove(id_obj=dish_id)
    return {'status': True, 'message': 'The dish has been deleted'}
