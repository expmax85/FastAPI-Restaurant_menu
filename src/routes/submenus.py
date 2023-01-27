from uuid import UUID

from fastapi import HTTPException, APIRouter, status


from src.database import actions
from src.models import schemas


router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=["Submenus"])


@router.post("/", response_model=schemas.SubMenu, status_code=status.HTTP_201_CREATED)
async def create_submenu(menu_id: UUID, submenu: schemas.SubMenuCreate):
    if not await actions.menu_orm.check_exist(menu_id):
        raise HTTPException(detail="menu not exists", status_code=404)
    return await actions.submenu_orm.create(obj_in=submenu, menu_id=menu_id)


@router.get('/{submenu_id}', response_model=schemas.SubMenu)
async def get_submenu(menu_id: UUID, submenu_id: UUID):
    if not (result := await actions.submenu_orm.get_with_relates(submenu_id=submenu_id, menu_id=menu_id)):
        raise HTTPException(detail="submenu not found", status_code=404)
    return result


@router.get('/', response_model=list[schemas.SubMenu])
async def get_submenus(menu_id: UUID, skip: int = 0, limit: int = 100):
    return await actions.submenu_orm.get_all_with_relates(menu_id=menu_id, skip=skip, limit=limit)


@router.patch("/{submenu_id}", response_model=schemas.SubMenu)
async def update_submenu(menu_id: UUID, submenu_id: UUID, submenu: schemas.SubMenuUpdate):
    if not await actions.submenu_orm.check_exist(menu_id=menu_id, submenu_id=submenu_id):
        raise HTTPException(detail="submenu not found", status_code=404)
    await actions.submenu_orm.update(id_obj=submenu_id, obj_data=submenu)
    return await actions.submenu_orm.get_with_relates(submenu_id=submenu_id, menu_id=menu_id)


@router.delete("/{submenu_id}", response_model=schemas.Remove)
async def delete_submenu(menu_id: UUID, submenu_id: UUID):
    if not await actions.submenu_orm.check_exist(menu_id=menu_id, submenu_id=submenu_id):
        raise HTTPException(detail="submenu not found", status_code=404)
    return {'status': await actions.submenu_orm.remove(id_obj=submenu_id),
            'message': 'The submenu has been deleted'}
