from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db, actions
from src.models import schemas


router = APIRouter(tags=["Dishes"])


@router.post("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=schemas.Dish,
             status_code=status.HTTP_201_CREATED)
async def create_dish(menu_id: str, submenu_id: str, dish: schemas.DishCreate,
                      db: AsyncSession = Depends(get_db)):
    existed = await actions.submenu_orm.check_exist(db=db, submenu_id=submenu_id, menu_id=menu_id,
                                                    with_relates=True)
    if not existed:
        raise HTTPException(detail="submenu for not found", status_code=404)
    result = await actions.dish_orm.create(db=db, obj_in=dish, submenu_id=submenu_id)
    return result


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[schemas.Dish])
async def get_dishes(menu_id: str, submenu_id: str, skip: int = 0, limit: int = 100,
                     db: AsyncSession = Depends(get_db)):
    result = await actions.dish_orm.get_all_with_relates(db=db, menu_id=menu_id,
                                                         submenu_id=submenu_id,
                                                         skip=skip, limit=limit)
    return result


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
async def get_dish(menu_id: str, submenu_id: str, dish_id: str,
                   db: AsyncSession = Depends(get_db)):
    result = await actions.dish_orm.get_with_relates(db=db, menu_id=menu_id,
                                                     submenu_id=submenu_id, dish_id=dish_id)
    if not result:
        raise HTTPException(detail="dish not found", status_code=404)
    return result


@router.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
async def update_dish(menu_id: str, submenu_id: str, dish_id: str, dish: schemas.DishUpdate,
                      db: AsyncSession = Depends(get_db)):
    existed = await actions.dish_orm.check_exist(db=db, dish_id=dish_id, menu_id=menu_id,
                                                 submenu_id=submenu_id,
                                                 with_relates=True)
    if not existed:
        raise HTTPException(detail="dish not found", status_code=404)
    await actions.dish_orm.update(db=db, id_obj=dish_id, obj_data=dish)
    result = await actions.dish_orm.get_with_relates(db=db, dish_id=dish_id, menu_id=menu_id,
                                                     submenu_id=submenu_id)
    return result


@router.delete("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(menu_id: str, submenu_id: str, dish_id: str,
                      db: AsyncSession = Depends(get_db)):
    existed = await actions.dish_orm.check_exist(db=db, dish_id=dish_id, menu_id=menu_id,
                                                 submenu_id=submenu_id,
                                                 with_relates=True)
    if not existed:
        raise HTTPException(detail="dish not found", status_code=404)
    await actions.dish_orm.remove(db=db, id_obj=dish_id)
    return {'status': True, 'message': 'The dish has been deleted'}
