from pydantic import BaseModel, validator
from pydantic.schema import UUID


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    title: str | None
    description: str | None


class Menu(MenuBase):
    id: UUID
    submenus_count: int | None = 0
    dishes_count: int | None = 0

    class Config:
        orm_mode = True

    @validator('id', check_fields=False)
    def id_to_str(cls, i):
        return str(i)


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    pass


class SubMenuUpdate(SubMenuBase):
    title: str | None
    description: str | None


class SubMenu(SubMenuBase):
    id: UUID
    dishes_count: int | None = 0

    class Config:
        orm_mode = True

    @validator('id', check_fields=False)
    def id_to_str(cls, i):
        return str(i)


class DishBase(BaseModel):
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    title: str | None
    description: str | None
    price: float | None


class Dish(DishBase):
    id: UUID

    class Config:
        orm_mode = True

    @validator('id', check_fields=False)
    def id_to_str(cls, i):
        return str(i)

    @validator('price', check_fields=False)
    def price_to_str(cls, price):
        return str(price)
