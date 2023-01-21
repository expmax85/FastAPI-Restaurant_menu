from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from src.database import get_db, actions
from src.models import schemas


router = APIRouter(tags=["Dishes"])


@router.post("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=schemas.Dish,
             status_code=status.HTTP_201_CREATED)
def create_dish(menu_id: str, submenu_id: str, dish: schemas.DishCreate, db: Session = Depends(get_db)) -> schemas.Dish:
    if not actions.submenu_orm.check_exist_relates(db, submenu_id, menu_id):
        raise HTTPException(detail="submenu for not found", status_code=404)
    dish = actions.dish_orm.create(db=db, obj_in=dish, submenu_id=submenu_id)
    return dish


@router.delete("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    if not actions.dish_orm.check_exist_relates(db=db, dish_id=dish_id, submenu_id=submenu_id, menu_id=menu_id):
        raise HTTPException(detail="dish not found", status_code=404)
    actions.dish_orm.remove(db=db, id_obj=dish_id)
    return {'status': True, 'message': 'The dish has been deleted'}


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[schemas.Dish])
def get_dishes(menu_id: str, submenu_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dishes = actions.dish_orm.get_all_with_relates(db=db, menu_id=menu_id, submenu_id=submenu_id,
                                                   skip=skip, limit=limit)
    return dishes


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def get_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    dish = actions.dish_orm.get_with_relates(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if not dish:
        raise HTTPException(detail="dish not found", status_code=404)
    return dish


@router.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def update_dish(menu_id: str, submenu_id: str, dish_id: str, dish: schemas.DishUpdate, db: Session = Depends(get_db)):
    if not actions.dish_orm.check_exist_relates(db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id):
        raise HTTPException(detail="dish not found", status_code=404)
    actions.dish_orm.update(db=db, id_obj=dish_id, obj_data=dish)
    dish = actions.dish_orm.get_with_relates(db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id)
    return dish
