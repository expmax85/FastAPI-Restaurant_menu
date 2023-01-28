from uuid import UUID

from fastapi import HTTPException

from src.database.actions import SubMenuAction
from src.models import schemas, SubMenu
from src.cache import serialize, key_gen, cache


class SubMenuService:
    all_cache_key = 'all_submenus'
    cache = cache
    service_orm = SubMenuAction()

    async def create(self, menu_id: UUID, data: schemas.SubMenuCreate) -> SubMenu:
        submenu = await self.service_orm.create(obj_in=data, menu_id=menu_id)
        values = serialize(submenu)
        values['dishes_count'] = 0
        await self.cache.set_cache(data=values, key=key_gen(menu_id, getattr(submenu, 'id')))
        await self.cache.delete_cache(key=key_gen(menu_id, self.all_cache_key))
        await self.cache.delete_cache(key=key_gen('all_menus'))
        await self.cache.delete_cache(key=key_gen(menu_id))
        return submenu

    async def get_list(self, menu_id: UUID, skip: int = 0, limit: int = 10) -> list[SubMenu] | dict:
        submenus = await self.cache.get_cache(key=key_gen(menu_id, self.all_cache_key))
        if not submenus:
            submenus = await self.service_orm.get_all_with_relates(menu_id=menu_id, skip=skip, limit=limit)
            values = list(serialize(submenu) for submenu in submenus)
            await self.cache.set_cache(data=values, key=key_gen(menu_id, self.all_cache_key))
        return submenus

    async def get(self, menu_id: UUID, submenu_id: UUID) -> SubMenu | dict:
        submenu = await self.cache.get_cache(key=key_gen(menu_id, submenu_id))
        if not submenu:
            submenu = await self.service_orm.get_with_relates(menu_id=menu_id, submenu_id=submenu_id)
            if not submenu:
                raise HTTPException(detail='submenu not found', status_code=404)
            await self.cache.set_cache(data=serialize(submenu), key=key_gen(menu_id, submenu_id))
        return submenu

    async def update(self, menu_id: UUID, submenu_id: UUID, data: schemas.SubMenuUpdate) -> dict:
        if not await self.service_orm.check_exist(menu_id=menu_id, submenu_id=submenu_id):
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


submenu_service = SubMenuService()
