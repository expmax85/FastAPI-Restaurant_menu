from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db, actions
from src.models import schemas


router = APIRouter(tags=["Submenus"])


@router.post("/menus/{menu_id}/submenus", response_model=schemas.SubMenu, status_code=status.HTTP_201_CREATED)
async def create_submenu(menu_id: str, submenu: schemas.SubMenuCreate, db: AsyncSession = Depends(get_db)):
    existed = await actions.menu_orm.check_exist(db, menu_id)
    if not existed:
        raise HTTPException(detail="menu not found", status_code=404)
    result = await actions.submenu_orm.create(db=db, obj_in=submenu, menu_id=menu_id)
    return result


@router.get('/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubMenu)
async def get_submenu(menu_id: str, submenu_id: str, db: AsyncSession = Depends(get_db)):
    result = await actions.submenu_orm.get_with_relates(db=db, submenu_id=submenu_id, menu_id=menu_id)
    if not result:
        raise HTTPException(detail="submenu not found", status_code=404)
    return result


@router.get('/menus/{menu_id}/submenus', response_model=list[schemas.SubMenu])
async def get_submenus(menu_id: str, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await actions.submenu_orm.get_all_with_relates(db=db, menu_id=menu_id, skip=skip, limit=limit)
    return result


@router.patch("/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenu)
async def update_submenu(menu_id: str, submenu_id: str, submenu: schemas.SubMenuUpdate,
                         db: AsyncSession = Depends(get_db)):
    existed = await actions.submenu_orm.check_exist(db=db, menu_id=menu_id, submenu_id=submenu_id,
                                                    with_relates=True)
    if not existed:
        raise HTTPException(detail="submenu not found", status_code=404)
    await actions.submenu_orm.update(db=db, id_obj=submenu_id, obj_data=submenu)
    result = await actions.submenu_orm.get_with_relates(db=db, submenu_id=submenu_id, menu_id=menu_id)
    return result


@router.delete("/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(menu_id: str, submenu_id: str, db: AsyncSession = Depends(get_db)):
    existed = await actions.submenu_orm.check_exist(db=db, menu_id=menu_id, submenu_id=submenu_id,
                                                    with_relates=True)
    if not existed:
        raise HTTPException(detail="submenu not found", status_code=404)
    await actions.submenu_orm.remove(db=db, id_obj=submenu_id)
    return {'status': True, 'message': 'The submenu has been deleted'}
