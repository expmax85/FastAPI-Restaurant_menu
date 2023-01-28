from uuid import UUID

from fastapi import HTTPException

from src.database.actions import MenuAction
from src.models import Menu, schemas
from src.cache import serialize, key_gen, cache


class MenuService:
    all_cache_key = 'all_menus'
    cache = cache
    menu_orm = MenuAction()

    async def create(self, data: schemas.MenuCreate) -> Menu:
        menu = await self.menu_orm.create(data)
        values = serialize(menu)
        values['submenus_count'] = 0
        values['dishes_count'] = 0
        await self.cache.set_cache(values, key=key_gen(menu.id))
        await self.cache.delete_cache(key=key_gen(self.all_cache_key))

        return menu

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Menu]:
        menus = await self.cache.get_cache(key=key_gen(self.all_cache_key))
        if not menus:
            menus = await self.menu_orm.get_all_with_relates(skip=skip, limit=limit)
            values = list(serialize(menu) for menu in menus)
            await self.cache.set_cache(data=values, key=key_gen(self.all_cache_key))
        return menus

    async def get(self, menu_id: UUID) -> Menu:
        menu = await self.cache.get_cache(key=key_gen(menu_id))
        if not menu:
            menu = await self.menu_orm.get_with_relates(menu_id=menu_id)
            if not menu:
                raise HTTPException(detail="menu not found", status_code=404)
            await self.cache.set_cache(data=serialize(menu), key=key_gen(menu_id))
        return menu

    async def update(self, menu_id: UUID, data: schemas.MenuUpdate) -> Menu:
        if not await self.menu_orm.check_exist(menu_id=menu_id):
            raise HTTPException(detail="menu not found", status_code=404)
        await self.cache.delete_cache(key=key_gen(menu_id))
        await self.menu_orm.update(id_obj=menu_id, obj_data=data)
        return await self.get(menu_id=menu_id)

    async def remove(self, menu_id: UUID) -> bool:
        await self.menu_orm.remove(id_obj=menu_id)
        await self.cache.delete_cache(key=key_gen(menu_id))
        await self.cache.delete_cache(key=key_gen(self.all_cache_key))
        await self.cache.delete_all(key_parent=key_gen(menu_id))
        return True


menu_service = MenuService()
