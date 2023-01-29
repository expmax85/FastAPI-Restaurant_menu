from src.database import actions
from src.database import SQLSession
from src.models import Dish
from src.models import Menu
from src.models import SubMenu

menu_orm = actions.MenuAction(model=Menu, db=SQLSession())
submenu_orm = actions.SubMenuAction(SubMenu, SQLSession())
dish_orm = actions.DishAction(Dish, SQLSession())
