from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException

from src.cache import get_cache
from src.cache import key_gen
from src.cache import serialize
from src.cache.cache_service import AbstractCache
from src.database.actions import get_menu_orm
from src.database.crud import BaseORM
from src.models import Menu
from src.models import schemas
from src.services.base_servises import Service


class MenuService(Service):
    def __init__(self, cache, service_orm, cache_key: str = 'all_dishes'):
        self.cache = cache
        self.service_orm = service_orm
        self.all_cache_key = cache_key

    async def create(self, data: schemas.MenuCreate) -> dict:
        menu = await self.service_orm.create(data)
        result = serialize(obj=menu)
        result['submenus_count'] = 0
        result['dishes_count'] = 0
        await self.cache.set_cache(result, key=key_gen(getattr(menu, 'id')))
        await self.cache.delete_cache(key=key_gen(self.all_cache_key))
        return result

    async def get_list(self, skip: int = 0, limit: int = 10) -> list | dict | None:
        result: list | dict | None = await self.cache.get_cache(key=key_gen(self.all_cache_key))
        if not result:
            menus: list[Menu] = await self.service_orm.get_all_with_relates(skip=skip, limit=limit)
            result = list([serialize(menu) for menu in menus])
            await self.cache.set_cache(data=result, key=key_gen(self.all_cache_key))
        return result

    async def get(self, menu_id: UUID) -> dict:
        result = await self.cache.get_cache(key=key_gen(menu_id))
        if not result:
            menu = await self.service_orm.get_with_relates(menu_id=menu_id)
            if not menu:
                raise HTTPException(detail='menu not found', status_code=404)
            result = serialize(menu)
            await self.cache.set_cache(data=result, key=key_gen(menu_id))
        return result

    async def update(self, menu_id: UUID, data: schemas.MenuUpdate) -> dict:
        if not await self.service_orm.check_exist_menu(menu_id=menu_id):
            raise HTTPException(detail='menu not found', status_code=404)
        await self.cache.delete_cache(key=key_gen(menu_id))
        await self.service_orm.update(id_obj=menu_id, obj_data=data)
        return await self.get(menu_id=menu_id)

    async def remove(self, menu_id: UUID) -> bool:
        await self.service_orm.remove(id_obj=menu_id)
        await self.cache.delete_cache(key=key_gen(menu_id))
        await self.cache.delete_cache(key=key_gen(self.all_cache_key))
        await self.cache.delete_all(key_parent=key_gen(menu_id))
        return True


def get_menu_service(cache: AbstractCache = Depends(get_cache),
                     service_orm: BaseORM = Depends(get_menu_orm)) -> Service:
    return MenuService(cache=cache, service_orm=service_orm)
