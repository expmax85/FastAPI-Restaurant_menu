from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    title: str | None
    description: str | None


class Menu(MenuBase):
    id: int
    submenus_count: int | None = 0
    dishes_count: int | None = 0

    class Config:
        orm_mode = True


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    pass


class SubMenuUpdate(SubMenuBase):
    title: str | None
    description: str | None


class SubMenu(SubMenuBase):
    id: int
    dishes_count: int | None = 0

    class Config:
        orm_mode = True


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
    id: int

    class Config:
        orm_mode = True
