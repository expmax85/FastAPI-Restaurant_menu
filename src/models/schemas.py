from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


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
    pass


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
    pass


class Dish(DishBase):
    id: int
    submenu_id: int | None = None

    class Config:
        orm_mode = True
