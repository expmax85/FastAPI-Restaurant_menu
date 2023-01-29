from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from src.models import schemas
from src.services import get_menu_service
from src.services import MenuService

router = APIRouter(prefix='/menus', tags=['Menus'])


@router.post('/', response_model=schemas.Menu, status_code=status.HTTP_201_CREATED)
async def create_menu(menu: schemas.MenuCreate,
                      menu_service: MenuService = Depends(get_menu_service)):
    """
    Create menu with all the information:

    - **title**: each menu must have a title
    - **description**: a long description
    """
    return await menu_service.create(data=menu)


@router.get('/', response_model=list[schemas.Menu])
async def get_menus(skip: int = 0, limit: int = 100,
                    menu_service: MenuService = Depends(get_menu_service)):
    """
    Get all menus
    """
    return await menu_service.get_list(skip=skip, limit=limit)


@router.get('/{menu_id}', response_model=schemas.Menu, responses={
    404: {
        'model': schemas.MenuError,
        'description': 'Menu not found'
    }
}
            )
async def get_menu(menu_id: UUID,
                   menu_service: MenuService = Depends(get_menu_service)):
    """
    Get menu by id
    """
    return await menu_service.get(menu_id=menu_id)


@router.patch('/{menu_id}', response_model=schemas.Menu, responses={
    404: {
        'model': schemas.MenuError,
        'description': 'Menu not found'
    }
}
            )
async def update_menu(menu_id: UUID, menu: schemas.MenuUpdate,
                      menu_service: MenuService = Depends(get_menu_service)):
    """
    Update menu and return updating instance
    """
    return await menu_service.update(menu_id=menu_id, data=menu)


@router.delete('/{menu_id}', response_model=schemas.Remove)
async def delete_menu(menu_id: UUID,
                      menu_service: MenuService = Depends(get_menu_service)):
    """
    Remove menu
    """
    return {
        'status': await menu_service.remove(menu_id=menu_id),
        'message': 'The menu has been deleted',
    }
