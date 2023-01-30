from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException

from src.cache import get_cache
from src.cache import key_gen
from src.cache.cache_service import AbstractCache
from src.config import settings
from src.database.actions import get_submenu_orm
from src.database.actions import SubMenuAction
from src.models import schemas
from src.models import SubMenu
from src.services.base_servises import Service


class SubMenuService(Service):
    def __init__(self, cache: AbstractCache, service_orm: SubMenuAction, cache_key: str):
        self.cache = cache
        self.service_orm = service_orm
        self.all_cache_key = cache_key

    async def create(self, menu_id: UUID, data: schemas.SubMenuCreate) -> dict:
        if not await self.service_orm.check_exist_menu(menu_id):
            raise HTTPException(detail='menu not found', status_code=404)
        submenu = await self.service_orm.create(obj_in=data, menu_id=menu_id)
        result: dict = self.service_orm.serialize(submenu)
        await self.cache.set_cache(data=result, key=key_gen(menu_id, result.get('id')))
        await self.cache.delete_cache(key=key_gen(menu_id, self.all_cache_key))
        await self.cache.delete_cache(key=key_gen(settings.App.MENU_CACHE_KEY))
        await self.cache.delete_cache(key=key_gen(menu_id))
        return result

    async def get_list(self, menu_id: UUID, skip: int = 0, limit: int = 10) -> list | dict:
        result: list | dict | None = await self.cache.get_cache(key=key_gen(menu_id, self.all_cache_key))
        if not result:
            submenus: list[SubMenu] = await self.service_orm.get_all_with_relates(menu_id=menu_id, skip=skip,
                                                                                  limit=limit)
            result = list(self.service_orm.serialize(submenu) for submenu in submenus)
            await self.cache.set_cache(data=result, key=key_gen(menu_id, self.all_cache_key))
        return result

    async def get(self, menu_id: UUID, submenu_id: UUID) -> dict:
        result: dict = await self.cache.get_cache(key=key_gen(menu_id, submenu_id))
        if not result:
            submenu: SubMenu = await self.service_orm.get_with_relates(menu_id=menu_id, submenu_id=submenu_id)
            if not submenu:
                raise HTTPException(detail='submenu not found', status_code=404)
            result = self.service_orm.serialize(submenu)
            await self.cache.set_cache(data=result, key=key_gen(menu_id, submenu_id))
        return result

    async def update(self, menu_id: UUID, submenu_id: UUID, data: schemas.SubMenuUpdate) -> dict:
        if not await self.service_orm.check_exist_submenu(menu_id=menu_id, submenu_id=submenu_id):
            raise HTTPException(detail='submenu not found', status_code=404)
        await self.cache.delete_cache(key=key_gen(menu_id, submenu_id))
        await self.service_orm.update(id_obj=submenu_id, obj_data=data)
        return await self.get(submenu_id=submenu_id, menu_id=menu_id)

    async def remove(self, menu_id: UUID, submenu_id: UUID) -> bool:
        await self.service_orm.remove(id_obj=submenu_id)
        await self.cache.delete_cache(key=key_gen(menu_id, submenu_id))
        await self.cache.delete_cache(key=key_gen(menu_id, self.all_cache_key))
        await self.cache.delete_many(key_parent=key_gen(menu_id, submenu_id))
        return True


def get_submenu_service(cache: AbstractCache = Depends(get_cache),
                        service_orm: SubMenuAction = Depends(get_submenu_orm)) -> Service:
    return SubMenuService(cache=cache, service_orm=service_orm, cache_key=settings.App.SUBMENU_CACHE_KEY)
