from uuid import UUID

from fastapi import HTTPException, APIRouter, status


from src.database import actions
from src.models import schemas
from src.services import submenu_service

router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=["Submenus"])


@router.post("/", response_model=schemas.SubMenu, status_code=status.HTTP_201_CREATED)
async def create_submenu(menu_id: UUID, submenu: schemas.SubMenuCreate):
    if not await actions.menu_orm.check_exist(menu_id):
        raise HTTPException(detail="menu not exists", status_code=404)
    return await submenu_service.create(data=submenu, menu_id=menu_id)


@router.get('/{submenu_id}', response_model=schemas.SubMenu)
async def get_submenu(menu_id: UUID, submenu_id: UUID):
    return await submenu_service.get(submenu_id=submenu_id, menu_id=menu_id)


@router.get('/', response_model=list[schemas.SubMenu])
async def get_submenus(menu_id: UUID, skip: int = 0, limit: int = 100):
    return await submenu_service.get_list(menu_id=menu_id, skip=skip, limit=limit)


@router.patch("/{submenu_id}", response_model=schemas.SubMenu)
async def update_submenu(menu_id: UUID, submenu_id: UUID, submenu: schemas.SubMenuUpdate):
    if not await actions.submenu_orm.check_exist(menu_id=menu_id, submenu_id=submenu_id):
        raise HTTPException(detail="submenu not found", status_code=404)
    return await submenu_service.update(submenu_id=submenu_id, menu_id=menu_id, data=submenu)


@router.delete("/{submenu_id}", response_model=schemas.Remove)
async def delete_submenu(menu_id: UUID, submenu_id: UUID):
    return {'status': await submenu_service.remove(menu_id=menu_id, submenu_id=submenu_id),
            'message': 'The submenu has been deleted'}
