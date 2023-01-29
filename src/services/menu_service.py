from uuid import UUID

from fastapi import HTTPException

from src.cache import cache
from src.cache import key_gen
from src.cache import RedisCache
from src.cache import serialize
from src.database.actions import MenuAction
from src.models import Menu
from src.models import schemas


class MenuService:
    all_cache_key: str = 'all_menus'
    cache: RedisCache = cache
    service_orm: MenuAction = MenuAction()

    async def create(self, data: schemas.MenuCreate) -> dict:
        menu = await self.service_orm.create(data)
        result = serialize(menu)
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
        if not await self.service_orm.check_exist(menu_id=menu_id):
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


menu_service = MenuService()
