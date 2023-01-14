from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database.crud import BaseCRUD
from src.models import schemas, Menu, SubMenu, Dish


class MenuAction(BaseCRUD[Menu, schemas.MenuCreate, schemas.MenuUpdate]):
    model = Menu

    def check_exist(self, db: Session, menu_id) -> bool:
        return db.query(db.query(self.model).filter(self.model.id == menu_id).exists()).scalar()

    def _get_subquery_dishes(self, db: Session):
        return db.query(SubMenu.menu_id.label('menu_id'),
                        func.coalesce(func.count(SubMenu.dishes), 0).label('dishes'))\
                 .outerjoin(Dish)\
                 .group_by(SubMenu.menu_id)\
                 .subquery()

    def get_all_with_relates(self, db: Session, skip: int = 0, limit: int = 100) -> list[tuple]:
        sq = self._get_subquery_dishes(db)
        queryset = db.query(self.model.id, self.model.title, self.model.description,
                            func.count(self.model.submenus).label('submenus_count'),
                            func.coalesce(sq.c.dishes, 0).label('dishes_count')) \
                     .outerjoin(SubMenu, SubMenu.menu_id == self.model.id) \
                     .outerjoin(sq, sq.c.menu_id == self.model.id) \
                     .group_by(self.model.id, sq.c.dishes) \
                     .offset(skip) \
                     .limit(limit) \
                     .all()
        return queryset

    def get_with_relates(self, db: Session, menu_id: int) -> tuple | None:
        sq = self._get_subquery_dishes(db)
        queryset = db.query(self.model.id, self.model.title, self.model.description,
                            func.count(self.model.submenus).label('submenus_count'),
                            func.coalesce(sq.c.dishes, 0).label('dishes_count')) \
                     .outerjoin(SubMenu, SubMenu.menu_id == self.model.id) \
                     .outerjoin(sq, sq.c.menu_id == self.model.id) \
                     .group_by(self.model.id, sq.c.dishes) \
                     .filter(self.model.id == menu_id) \
                     .first()
        if not queryset or not any(queryset):
            return None
        return queryset

    def serialize(self, obj: Menu) -> dict:
        data = super().serialize(obj)
        if hasattr(obj, 'submenus_count'):
            data['submenus_count'] = obj.submenus_count
        else:
            data['submenus_count'] = 0
        if hasattr(obj, 'dishes_count'):
            data['dishes_count'] = obj.dishes_count
        else:
            data['dishes_count'] = 0
        return data


class SubMenuAction(BaseCRUD[SubMenu, schemas.SubMenuCreate, schemas.SubMenuUpdate]):
    model = SubMenu

    def check_exist_relates(self, db: Session, submenu_id, menu_id) -> bool:
        return db.query(
            db.query(self.model).filter(self.model.id == submenu_id, self.model.menu_id == menu_id).exists()).scalar()

    def get_with_relates(self, db: Session, submenu_id: int, menu_id: int) -> tuple:
        return db.query(self.model.id, self.model.title, self.model.description,
                        func.coalesce(func.count(Dish.id), 0).label('dishes_count')) \
            .outerjoin(Dish, self.model.id == Dish.submenu_id) \
            .filter(self.model.id == submenu_id, self.model.menu_id == menu_id) \
            .group_by(self.model.id).first()

    def get_all_with_relates(self, db: Session, menu_id: int, skip: int = 0, limit: int = 100) -> list[tuple]:
        return db.query(self.model.id, self.model.title, self.model.description,
                        func.coalesce(func.count(Dish.id), 0).label('dishes_count')) \
            .outerjoin(Dish, self.model.id == Dish.submenu_id) \
            .filter(self.model.menu_id == menu_id) \
            .group_by(self.model.id) \
            .offset(skip).limit(limit).all()

    def serialize(self, obj: SubMenu) -> dict:
        data = super().serialize(obj)
        if hasattr(obj, 'dishes_count'):
            data['dishes_count'] = obj.dishes_count
        else:
            data['dishes_count'] = 0
        return data


class DishAction(BaseCRUD[Dish, schemas.DishCreate, schemas.DishUpdate]):
    model = Dish

    def check_exist_relates(self, db: Session, submenu_id, menu_id, dish_id) -> bool:
        return db.query(db.query(self.model)
                          .join(SubMenu, SubMenu.id == self.model.submenu_id)
                          .filter(self.model.id == dish_id,
                                  SubMenu.id == submenu_id,
                                  SubMenu.menu_id == menu_id)
                 .exists()).scalar()

    def get_with_relates(self, db: Session, dish_id: int, submenu_id: int, menu_id: int) -> Dish:
        return db.query(self.model).join(SubMenu, SubMenu.id == self.model.submenu_id) \
            .filter(self.model.id == dish_id,
                    self.model.submenu_id == submenu_id,
                    SubMenu.menu_id == menu_id) \
            .first()

    def get_all_with_relates(self, db: Session, menu_id: int, submenu_id: int, skip: int, limit: int) -> list[Dish]:
        return db.query(self.model).join(SubMenu, SubMenu.id == self.model.submenu_id) \
            .filter(self.model.submenu_id == submenu_id,
                    SubMenu.menu_id == menu_id) \
            .offset(skip).limit(limit).all()

    def serialize(self, obj: Dish) -> dict:
        data = super().serialize(obj)
        if hasattr(obj, 'price'):
            data['price'] = str(obj.price)
        return data


menu_orm = MenuAction()
submenu_orm = SubMenuAction()
dish_orm = DishAction()
