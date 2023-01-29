from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException

from src.cache import get_cache
from src.cache import key_gen
from src.cache import serialize
from src.cache.cache_service import AbstractCache
from src.database.actions import get_submenu_orm
from src.database.crud import BaseORM
from src.models import schemas
from src.models import SubMenu
from src.services.base_servises import Service


class SubMenuService(Service):
    def __init__(self, cache, service_orm, cache_key: str = 'all_dishes'):
        self.cache = cache
        self.service_orm = service_orm
        self.all_cache_key = cache_key

    async def create(self, menu_id: UUID, data: schemas.SubMenuCreate) -> dict:
        submenu = await self.service_orm.create(obj_in=data, menu_id=menu_id)
        result: dict = serialize(submenu)
        result['dishes_count'] = 0
        await self.cache.set_cache(data=result, key=key_gen(menu_id, getattr(submenu, 'id')))
        await self.cache.delete_cache(key=key_gen(menu_id, self.all_cache_key))
        await self.cache.delete_cache(key=key_gen('all_menus'))
        await self.cache.delete_cache(key=key_gen(menu_id))
        return result

    async def get_list(self, menu_id: UUID, skip: int = 0, limit: int = 10) -> list | dict | None:
        result: list | dict | None = await self.cache.get_cache(key=key_gen(menu_id, self.all_cache_key))
        if not result:
            submenus: list[SubMenu] = await self.service_orm.get_all_with_relates(menu_id=menu_id, skip=skip,
                                                                                  limit=limit)
            result = list(serialize(submenu) for submenu in submenus)
            await self.cache.set_cache(data=result, key=key_gen(menu_id, self.all_cache_key))
        return result

    async def get(self, menu_id: UUID, submenu_id: UUID) -> dict:
        result: dict = await self.cache.get_cache(key=key_gen(menu_id, submenu_id))
        if not result:
            submenu: SubMenu = await self.service_orm.get_with_relates(menu_id=menu_id, submenu_id=submenu_id)
            if not submenu:
                raise HTTPException(detail='submenu not found', status_code=404)
            result = serialize(submenu)
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
        await self.cache.delete_all(key_parent=key_gen(menu_id))
        return True


def get_submenu_service(cache: AbstractCache = Depends(get_cache),
                        service_orm: BaseORM = Depends(get_submenu_orm)) -> Service:
    return SubMenuService(cache=cache, service_orm=service_orm)
