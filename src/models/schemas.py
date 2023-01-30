from pydantic import BaseModel
from pydantic import validator
from pydantic.schema import UUID


# Base schemas

class MenuBase(BaseModel):
    title: str
    description: str


class SubMenuBase(BaseModel):
    title: str
    description: str


class DishBase(BaseModel):
    title: str
    description: str
    price: float


class RemoveModel(BaseModel):
    status: bool = True
    message: str


class ModelError(BaseModel):
    detail: str


# Menus schemas

class MenuCreate(MenuBase):
    class Config:
        schema_extra = {
            'example': {
                'title': 'Test Menu',
                'description': 'A nice pretty menu for testing',
            }
        }


class MenuUpdate(MenuBase):
    title: str | None
    description: str | None

    class Config:
        schema_extra = {
            'example': {
                'title': 'Updated Test Menu',
                'description': 'You just now update it',
            }
        }


class Menu(MenuBase):
    id: UUID
    submenus_count: int | None = 0
    dishes_count: int | None = 0

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Test Menu',
                'description': 'A nice pretty menu for testing',
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'submenus_count': 0,
                'dishes_count': 0
            }
        }


class UpdatedMenu(Menu):
    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Updated Test Menu',
                'description': 'You just now update it',
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'submenus_count': 0,
                'dishes_count': 0
            }
        }


class MenuRemove(RemoveModel):
    class Config:
        schema_extra = {
            'example': {
                'status': True,
                'message': 'The menu has been deleted'
            }
        }


class MenuError(ModelError):
    class Config:
        schema_extra = {
            'example': {'detail': 'menu not found'}
        }


# Submenus schemas

class SubMenuCreate(SubMenuBase):
    class Config:
        schema_extra = {
            'example': {
                'title': 'Test Submenu',
                'description': 'A nice pretty submenu for testing',
            }
        }


class SubMenuUpdate(SubMenuBase):
    title: str | None
    description: str | None

    class Config:
        schema_extra = {
            'example': {
                'title': 'Updated Test Submenu',
                'description': 'You just now update it',
            }
        }


class SubMenu(SubMenuBase):
    id: UUID
    dishes_count: int | None = 0

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Test SubMenu',
                'description': 'A nice pretty submenu for testing',
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'submenus_count': 0,
                'dishes_count': 0
            }
        }


class UpdatedSubMenu(SubMenu):
    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Updated Test SubMenu',
                'description': 'You just now update it',
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'dishes_count': 0
            }
        }


class SubMenuRemove(RemoveModel):
    class Config:
        schema_extra = {
            'example': {
                'status': True,
                'message': 'The submenu has been deleted'
            }
        }


class SubMenuError(ModelError):
    class Config:
        schema_extra = {
            'example': {'detail': 'submenu not found'}
        }


# Dishes schemas

class DishCreate(DishBase):
    class Config:
        schema_extra = {
            'example': {
                'title': 'Test Dish',
                'description': 'A nice pretty dish for testing',
                'price': '10.0'
            }
        }


class DishUpdate(DishBase):
    title: str | None
    description: str | None
    price: float | None

    class Config:
        schema_extra = {
            'example': {
                'title': 'Updated Test Dish',
                'description': 'You just now update it',
                'price': '20.0'
            }
        }


class Dish(DishBase):
    id: UUID

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Test Dish',
                'description': 'A nice pretty dish for testing',
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'price': '10.0'
            }
        }

    @validator('price', check_fields=False)
    def price_to_str(cls, price):
        return str(price)


class UpdatedDish(Dish):
    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Updated Test Dish',
                'description': 'You just now update it',
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'price': '20.0'
            }
        }


class DishRemove(RemoveModel):
    class Config:
        schema_extra = {
            'example': {
                'status': True,
                'message': 'The dish has been deleted'
            }
        }


class DishError(ModelError):
    class Config:
        schema_extra = {
            'example': {'detail': 'dish not found'}
        }
