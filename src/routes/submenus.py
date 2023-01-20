from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.database import get_db, actions
from src.models import schemas


router = APIRouter(tags=["submenus"])


@router.post("/menus/{menu_id}/submenus", response_model=schemas.SubMenu)
def create_submenu(menu_id: int, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)):
    if not actions.menu_orm.check_exist(db, menu_id):
        raise HTTPException(detail="menu not found", status_code=404)
    submenu = actions.submenu_orm.create(db=db, obj_in=submenu, menu_id=menu_id)
    result = actions.submenu_orm.serialize(submenu)
    return JSONResponse(result, status_code=201)


@router.get('/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubMenu)
def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = actions.submenu_orm.get_with_relates(db=db, submenu_id=submenu_id, menu_id=menu_id)
    if not submenu:
        raise HTTPException(detail="submenu not found", status_code=404)
    return JSONResponse(actions.submenu_orm.serialize(submenu), status_code=200)


@router.get('/menus/{menu_id}/submenus', response_model=list[schemas.SubMenu])
def get_submenus(menu_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    submenus = actions.submenu_orm.get_all_with_relates(db=db, menu_id=menu_id, skip=skip, limit=limit)
    return submenus


@router.delete("/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    if not actions.submenu_orm.check_exist_relates(db, submenu_id, menu_id):
        raise HTTPException(detail="submenu not found", status_code=404)
    actions.submenu_orm.remove(db=db, id_obj=submenu_id)
    return JSONResponse({'status': True, 'message': 'The submenu has been deleted'}, status_code=200)


@router.patch("/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenu)
def update_submenu(menu_id: int, submenu_id: int, submenu: schemas.SubMenuUpdate, db: Session = Depends(get_db)):
    if not actions.submenu_orm.check_exist_relates(db, submenu_id, menu_id):
        raise HTTPException(detail="submenu not found", status_code=404)
    actions.submenu_orm.update(db=db, id_obj=submenu_id, obj_data=submenu)
    submenu = actions.submenu_orm.get_with_relates(db=db, submenu_id=submenu_id, menu_id=menu_id)
    return JSONResponse(actions.submenu_orm.serialize(submenu), status_code=200)