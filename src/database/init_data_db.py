import json
import os

from src.config import FIXTURES_DIR
from src.database import SQLSession
from src.models import Dish, Menu, SubMenu

async_session = SQLSession()


async def init_test_data_db() -> None:
    path = os.path.join(FIXTURES_DIR, "menus.json")
    with open(path, encoding="utf-8") as f:
        data = json.loads(f.read())
    async with async_session as db:
        menu_list = list()
        for item in data:
            menu = Menu(title=item["title"], description=item["description"])
            for sm in item["submenus"]:
                submenu = SubMenu(title=sm["title"], description=sm["description"])
                for dh in sm["dishes"]:
                    dish = Dish(**dh)
                    submenu.dishes.append(dish)
                menu.submenus.append(submenu)
            menu_list.append(menu)
        db.session.add_all(menu_list)
