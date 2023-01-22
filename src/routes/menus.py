from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db, actions
from src.models import schemas


router = APIRouter(tags=["Menus"])


@router.post("/menus", response_model=schemas.Menu, status_code=status.HTTP_201_CREATED)
async def create_menu(menu: schemas.MenuCreate, db: AsyncSession = Depends(get_db)):
    result = await actions.menu_orm.create(db=db, obj_in=menu)
    return result


@router.get("/menus", response_model=list[schemas.Menu])
async def get_menus(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await actions.menu_orm.get_all_with_relates(db=db, skip=skip, limit=limit)
    return result


@router.get("/menus/{menu_id}", response_model=schemas.Menu)
async def get_menu(menu_id: str, db: AsyncSession = Depends(get_db)):
    result = await actions.menu_orm.get_with_relates(db=db, menu_id=menu_id)
    if not result:
        raise HTTPException(detail="menu not found", status_code=404)
    return result


@router.patch("/menus/{menu_id}", response_model=schemas.Menu)
async def update_menu(menu_id: str, menu: schemas.MenuUpdate, db: AsyncSession = Depends(get_db)):
    existed = await actions.menu_orm.check_exist(db=db, menu_id=menu_id)
    if not existed:
        raise HTTPException(detail="menu not found", status_code=200)
    await actions.menu_orm.update(db=db, id_obj=menu_id, obj_data=menu)
    result = await actions.menu_orm.get_with_relates(db=db, menu_id=menu_id)
    return result


@router.delete("/menus/{menu_id}")
async def delete_menu(menu_id: str, db: AsyncSession = Depends(get_db)):
    existed = await actions.menu_orm.check_exist(db=db, menu_id=menu_id)
    if not existed:
        raise HTTPException(detail='menu not exists', status_code=404)
    await actions.menu_orm.remove(db=db, id_obj=menu_id)
    return {'status': True, 'message': 'The menu has been deleted'}
