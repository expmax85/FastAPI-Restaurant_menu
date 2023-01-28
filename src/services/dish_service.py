from uuid import UUID

from fastapi import HTTPException

from src.cache import serialize, key_gen, cache
from src.database.actions import DishAction
from src.models import schemas, Dish


class DishService:
    all_cache_key = 'all_dishes'
    cache = cache
    service_orm = DishAction()

    async def create(self, menu_id: UUID, submenu_id: UUID, data: schemas.DishCreate) -> Dish:
        dish = await self.service_orm.create(obj_in=data, submenu_id=submenu_id)
        values = serialize(dish)
        await self.cache.set_cache(data=values, key=key_gen(menu_id, submenu_id, dish.id))
        await self.cache.delete_cache(key=key_gen(menu_id, submenu_id, self.all_cache_key))
        await self.cache.delete_cache(key=key_gen(menu_id, 'all_submenus'))
        await self.cache.delete_cache(key=key_gen(menu_id, submenu_id))
        return dish

    async def get_list(self, menu_id: UUID, submenu_id: UUID, skip: int = 0, limit: int = 10) -> list[Dish]:
        cache_key = key_gen(menu_id, submenu_id, self.all_cache_key)
        dishes = await self.cache.get_cache(key=cache_key)
        if not dishes:
            dishes = await self.service_orm.get_all_with_relates(menu_id=menu_id, submenu_id=submenu_id,
                                                                 skip=skip, limit=limit)
            values = list(serialize(dish) for dish in dishes)
            await self.cache.set_cache(data=values, key=cache_key)
        return dishes

    async def get(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> Dish:
        cache_key = key_gen(menu_id, submenu_id, dish_id)
        dish = await self.cache.get_cache(key=cache_key)
        if not dish:
            dish = await self.service_orm.get_with_relates(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
            if not dish:
                raise HTTPException(detail="dish not found", status_code=404)

            await self.cache.set_cache(data=serialize(dish), key=cache_key)
        return dish

    async def update(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, data: schemas.DishUpdate) -> Dish:
        await self.cache.delete_cache(key=key_gen(menu_id, submenu_id, dish_id))
        await self.service_orm.update(id_obj=dish_id, obj_data=data)
        return await self.get(submenu_id=submenu_id, menu_id=menu_id, dish_id=dish_id)

    async def remove(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> bool:
        await self.service_orm.remove(id_obj=dish_id)
        await self.cache.delete_cache(key=key_gen(menu_id, submenu_id, dish_id))
        await self.cache.delete_cache(key=key_gen(menu_id, submenu_id, self.all_cache_key))
        await self.cache.delete_cache(key=key_gen(menu_id, 'all_menus'))
        await self.cache.delete_cache(key=key_gen(menu_id, submenu_id, 'all_submenus'))
        await self.cache.delete_cache(key=key_gen(menu_id, submenu_id))
        return True


dish_service = DishService()
