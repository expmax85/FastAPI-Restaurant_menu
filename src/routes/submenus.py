from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from src.models import schemas
from src.services import get_submenu_service
from src.services import Service


router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=['Submenus'])


@router.post('/', response_model=schemas.SubMenu, status_code=status.HTTP_201_CREATED,
             responses={
                 404: {
                     'model': schemas.MenuError,
                     'description': 'Menu not exist'
                 }
             }
             )
async def create_submenu(menu_id: UUID, submenu: schemas.SubMenuCreate,
                         submenu_service: Service = Depends(get_submenu_service)):
    """
    Create submenu  for menu with all the information:

    - **title**: each submenu must have a title
    - **description**: a long description
    """
    if not await submenu_service.service_orm.check_exist_menu(menu_id):
        raise HTTPException(detail='menu not found', status_code=404)
    return await submenu_service.create(data=submenu, menu_id=menu_id)


@router.get('/{submenu_id}', response_model=schemas.SubMenu,
            responses={
                404: {
                    'model': schemas.SubMenuError,
                    'description': 'Submenu not found. Check menu existing.'
                }
            }
            )
async def get_submenu(menu_id: UUID, submenu_id: UUID,
                      submenu_service: Service = Depends(get_submenu_service)):
    """
    Get submenu by id, depending on menu
    """
    return await submenu_service.get(submenu_id=submenu_id, menu_id=menu_id)


@router.get('/', response_model=list[schemas.SubMenu])
async def get_submenus(menu_id: UUID, skip: int = 0, limit: int = 100,
                       submenu_service: Service = Depends(get_submenu_service)):
    """
    Get all submenus, depending on menu
    """
    return await submenu_service.get_list(menu_id=menu_id, skip=skip, limit=limit)


@router.patch('/{submenu_id}', response_model=schemas.SubMenu, responses={
    404: {
        'model': schemas.SubMenuError,
        'description': 'Submenu not found'
    }
}
)
async def update_submenu(menu_id: UUID, submenu_id: UUID, submenu: schemas.SubMenuUpdate,
                         submenu_service: Service = Depends(get_submenu_service)):
    """
    Update submenu
    """
    if not await submenu_service.service_orm.check_exist_submenu(menu_id=menu_id, submenu_id=submenu_id):
        raise HTTPException(detail='submenu not found', status_code=404)
    return await submenu_service.update(submenu_id=submenu_id, menu_id=menu_id, data=submenu)


@router.delete('/{submenu_id}', response_model=schemas.Remove)
async def delete_submenu(menu_id: UUID, submenu_id: UUID,
                         submenu_service: Service = Depends(get_submenu_service)):
    """
    Remove submenu
    """
    await submenu_service.remove(menu_id=menu_id, submenu_id=submenu_id)
    return {
        'status': True,
        'message': 'The submenu has been deleted',
    }
