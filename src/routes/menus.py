from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from src.database import get_db, actions
from src.models import schemas


router = APIRouter(tags=["Menus"])


@router.post("/menus", response_model=schemas.Menu, status_code=status.HTTP_201_CREATED, responses={
    201: {
            "description": "Created",
            "content": {
                "application/json": {
                    "example": {"id": 0, "title": "string", "description": "string",
                                "submenus_count": 0, "dishes_count": 0}
                }
            }
        }
})
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    menu = actions.menu_orm.create(db=db, obj_in=menu)
    return menu


@router.get("/menus", response_model=list[schemas.Menu])
def get_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    menus = actions.menu_orm.get_all_with_relates(db=db, skip=skip, limit=limit)
    return menus


@router.get("/menus/{menu_id}", response_model=schemas.Menu)
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    menu = actions.menu_orm.get_with_relates(db=db, menu_id=menu_id)
    if not menu or not any(menu):
        raise HTTPException(detail="menu not found", status_code=404)
    return menu


@router.patch("/menus/{menu_id}", response_model=schemas.Menu)
def update_menu(menu_id: str, menu: schemas.MenuUpdate, db: Session = Depends(get_db)):
    updated = actions.menu_orm.update(db=db, id_obj=menu_id, obj_data=menu)
    if not updated:
        raise HTTPException(detail="menu not found", status_code=200)
    menu = actions.menu_orm.get_with_relates(db=db, menu_id=menu_id)
    return menu


@router.delete("/menus/{menu_id}")
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    if not actions.menu_orm.check_exist(db=db, menu_id=menu_id):
        raise HTTPException(detail='menu not exists', status_code=404)
    actions.menu_orm.remove(db=db, id_obj=menu_id)
    return {'status': True, 'message': 'The menu has been deleted'}
