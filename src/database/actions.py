from typing import Type
from uuid import UUID
from sqlalchemy import func, select, exists
from sqlalchemy.sql import Subquery

from src.database.crud import BaseCRUD
from src.models import Menu, SubMenu, Dish


class MenuAction(BaseCRUD):
    model: Type[Menu] = Menu

    async def check_exist(self, menu_id: UUID) -> bool:
        async with self.db as db:
            result = await db.session.execute(exists(self.model)
                                              .where(self.model.id == menu_id)
                                              .select())
        if result.scalars().first():
            return True
        return False

    async def _get_subquery_dishes(self) -> 'Subquery':
        return select(
            SubMenu.menu_id.label('menu_id'),
            func.coalesce(func.count(SubMenu.dishes), 0).label('dishes'),
        ) \
            .outerjoin(Dish) \
            .group_by(SubMenu.menu_id) \
            .subquery()

    async def _query_for_get(self, sq: 'Subquery') -> 'select':
        return select(
            self.model.id, self.model.title, self.model.description,
            func.count(self.model.submenus).label('submenus_count'),
            func.coalesce(sq.c.dishes, 0).label('dishes_count'),
        ) \
            .outerjoin(SubMenu, SubMenu.menu_id == self.model.id) \
            .outerjoin(sq, sq.c.menu_id == self.model.id) \
            .group_by(self.model.id, sq.c.dishes)

    async def get_all_with_relates(self, skip: int = 0, limit: int = 100) -> list[Menu]:
        async with self.db as db:
            sq = await self._get_subquery_dishes()
            queryset = await self._query_for_get(sq)
            result = await db.session.execute(queryset.offset(skip).limit(limit))
        return result.all()

    async def get_with_relates(self, menu_id: UUID) -> Menu | None:
        async with self.db as db:
            sq = await self._get_subquery_dishes()
            queryset = await self._query_for_get(sq)
            result = await db.session.execute(queryset.filter(self.model.id == menu_id))
        return result.first()


class SubMenuAction(BaseCRUD):
    model: Type[SubMenu] = SubMenu

    async def check_exist(self, submenu_id: UUID, menu_id: UUID) -> bool:
        async with self.db as db:
            result = await db.session.execute(
                exists(self.model)
                .where(
                    self.model.id == submenu_id,
                    self.model.menu_id == menu_id,
                ).select(),
            )
        if result.scalars().first():
            return True
        return False

    async def _query_for_get(self, menu_id: UUID) -> 'select':
        return select(
            self.model.id, self.model.title, self.model.description,
            func.coalesce(func.count(Dish.id), 0).label('dishes_count'),
        )\
            .outerjoin(Dish, self.model.id == Dish.submenu_id)\
            .group_by(self.model.id)\
            .filter(self.model.menu_id == menu_id)

    async def get_with_relates(self, submenu_id: UUID, menu_id: UUID) -> SubMenu | None:
        async with self.db as db:
            queryset = await self._query_for_get(menu_id)
            result = await db.session.execute(queryset.filter(self.model.id == submenu_id))
        return result.first()

    async def get_all_with_relates(self, menu_id: UUID, skip: int = 0,
                                   limit: int = 100) -> list[SubMenu]:
        async with self.db as db:
            queryset = await self._query_for_get(menu_id)
            result = await db.session.execute(queryset.offset(skip).limit(limit))
        return result.all()


class DishAction(BaseCRUD):
    model: Type[Dish] = Dish

    async def check_exist(self, submenu_id: UUID, dish_id: UUID) -> bool:
        async with self.db as db:
            result = await db.session.execute(
                select(
                    exists(self.model)
                    .where(
                        self.model.id == dish_id,
                        self.model.submenu_id == submenu_id,
                    ),
                )
                .select(),
            )
        if result.scalars().first():
            return True
        return False

    async def _query_for_get(self, menu_id: UUID, submenu_id: UUID) -> 'select':
        return select(self.model).join(SubMenu, SubMenu.id == self.model.submenu_id)\
            .filter(
                self.model.submenu_id == submenu_id,
                SubMenu.menu_id == menu_id,
        )

    async def get_with_relates(self, dish_id: UUID, submenu_id: UUID, menu_id: UUID) -> Dish:
        async with self.db as db:
            queryset = await self._query_for_get(menu_id, submenu_id)
            result = await db.session.execute(queryset.filter(self.model.id == dish_id))
        return result.scalars().first()

    async def get_all_with_relates(self, menu_id: UUID, submenu_id: UUID, skip: int, limit: int) -> list[Dish]:
        async with self.db as db:
            queryset = await self._query_for_get(menu_id, submenu_id)
            result = await db.session.execute(queryset.offset(skip).limit(limit))
        return result.scalars().all()


menu_orm = MenuAction()
submenu_orm = SubMenuAction()
dish_orm = DishAction()
