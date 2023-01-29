from pydantic import BaseModel
from pydantic import validator
from pydantic.schema import UUID


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass

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


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    pass

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


class DishBase(BaseModel):
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    pass

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

    @validator('price', check_fields=False)
    def price_to_str(cls, price):
        return str(price)


class Remove(BaseModel):
    status: bool = True
    message: str


class DishError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            'example': {'detail': 'dish not found'},
        }


class SubMenuError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            'example': {'detail': 'submenu not found'},
        }


class MenuError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            'example': {'detail': 'menu not found'},
        }
