from sqlalchemy import func, select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud import BaseCRUD
from src.models import schemas, Menu, SubMenu, Dish


class MenuAction(BaseCRUD[Menu, schemas.MenuCreate, schemas.MenuUpdate]):
    model = Menu

    async def check_exist(self, db: AsyncSession, menu_id: str) -> bool:
        result = await db.execute(exists(self.model).where(self.model.id == menu_id).select())
        if result.scalars().first():
            return True
        return False

    def _get_subquery_dishes(self):
        return select(SubMenu.menu_id.label('menu_id'),
                      func.coalesce(func.count(SubMenu.dishes), 0).label('dishes')) \
            .outerjoin(Dish) \
            .group_by(SubMenu.menu_id) \
            .subquery()

    def _query_for_get(self):
        sq = self._get_subquery_dishes()
        return select(self.model.id, self.model.title, self.model.description,
                      func.count(self.model.submenus).label('submenus_count'),
                      func.coalesce(sq.c.dishes, 0).label('dishes_count')) \
            .outerjoin(SubMenu, SubMenu.menu_id == self.model.id) \
            .outerjoin(sq, sq.c.menu_id == self.model.id) \
            .group_by(self.model.id, sq.c.dishes)

    async def get_all_with_relates(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[tuple]:
        queryset = self._query_for_get()
        result = await db.execute(queryset.offset(skip).limit(limit))
        return result.all()

    async def get_with_relates(self, db: AsyncSession, menu_id: str) -> tuple | None:
        queryset = self._query_for_get()
        result = await db.execute(queryset.filter(self.model.id == menu_id))
        return result.first()


class SubMenuAction(BaseCRUD[SubMenu, schemas.SubMenuCreate, schemas.SubMenuUpdate]):
    model = SubMenu

    async def check_exist(self, db: AsyncSession, submenu_id: str, menu_id: str, with_relates: bool = False) -> bool:
        if with_relates:
            result = await db.execute(exists(self.model).where(self.model.id == submenu_id,
                                                               self.model.menu_id == menu_id).select())
        else:
            result = await db.execute(exists(self.model).where(self.model.id == submenu_id).select())
        if result.scalars().first():
            return True
        return False

    def _query_for_get(self, menu_id: str):
        return select(self.model.id, self.model.title, self.model.description,
                      func.coalesce(func.count(Dish.id), 0).label('dishes_count'))\
            .outerjoin(Dish, self.model.id == Dish.submenu_id)\
            .group_by(self.model.id)\
            .filter(self.model.menu_id == menu_id)

    async def get_with_relates(self, db: AsyncSession, submenu_id: str, menu_id: str) -> tuple:
        queryset = self._query_for_get(menu_id)
        result = await db.execute(queryset.filter(self.model.id == submenu_id))
        return result.first()

    async def get_all_with_relates(self, db: AsyncSession, menu_id: str, skip: int = 0, limit: int = 100) -> list[tuple]:
        queryset = self._query_for_get(menu_id)
        result = await db.execute(queryset.offset(skip).limit(limit))
        return result.all()


class DishAction(BaseCRUD[Dish, schemas.DishCreate, schemas.DishUpdate]):
    model = Dish

    async def check_exist(self, db: AsyncSession, submenu_id: str, menu_id: str, dish_id: str, with_relates: bool = False) -> bool:
        if with_relates:
            pre_check = await db.execute(exists(self.model).where(self.model.id == submenu_id,
                                                                  self.model.menu_id == menu_id).select())
            if not pre_check.scalars().first():
                return False
            result = await db.execute(select(exists(self.model)
                                      .where(self.model.id == dish_id,
                                             self.model.submenu_id == submenu_id))
                                      .select())
        else:
            result = await db.execute(exists(self.model).where(self.model.id == dish_id).select())
        if result.scalars().first():
            return True
        return False

    def _query_for_get(self, menu_id: str, submenu_id: str):
        return select(self.model).join(SubMenu, SubMenu.id == self.model.submenu_id)\
                                .filter(self.model.submenu_id == submenu_id,
                                        SubMenu.menu_id == menu_id)

    async def get_with_relates(self, db: AsyncSession, dish_id: str, submenu_id: str, menu_id: str) -> Dish:
        queryset = self._query_for_get(menu_id, submenu_id)
        result = await db.execute(queryset.filter(self.model.id == dish_id))
        return result.scalars().first()

    async def get_all_with_relates(self, db: AsyncSession, menu_id: str, submenu_id: str, skip: int, limit: int) -> list[Dish]:
        queryset = self._query_for_get(menu_id, submenu_id)
        result = await db.execute(queryset.offset(skip).limit(limit))
        return result.scalars().all()


menu_orm = MenuAction()
submenu_orm = SubMenuAction()
dish_orm = DishAction()
