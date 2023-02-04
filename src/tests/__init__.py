from src.database import SQLSession, actions

menu_orm = actions.MenuAction(db=SQLSession())
submenu_orm = actions.SubMenuAction(db=SQLSession())
dish_orm = actions.DishAction(db=SQLSession())
