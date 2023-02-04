from src.database import SQLSession
from src.models import Dish, Menu, SubMenu

async_session = SQLSession()


async def init_test_data_db() -> None:
    async with async_session as db:
        menus = [
            Menu(title="Меню", description="Основное меню"),
            Menu(title="Напитки", description="Алкогольные напитки"),
        ]
        submenus_1 = [
            SubMenu(title="Горячие закуски", description="Наеться от души"),
            SubMenu(title="Холодные закуски", description="Перекусить перед едой"),
        ]
        submenus_2 = [
            SubMenu(title="Барное меню", description="Для компании в кругу друзей"),
            SubMenu(title="Винное меню", description="Для романтического вечера"),
        ]
        dishes_1_1 = [
            Dish(
                title="Спаржа с луком из пармезана",
                description="Сочетание несочетаемого",
                price=1100.00,
            ),
            Dish(
                title="Креветки в тембуре", description="Морское ассорти", price=850.00
            ),
        ]
        dishes_1_2 = [
            Dish(
                title="Мясное плато",
                description="Хамон, Пармская ветчинаб артишокиб маслины",
                price=2000.00,
            ),
            Dish(
                title="Сырное ассорти",
                description="Камамбер, Пармезан, виноград, клубника, грецкий орех, мед",
                price=1800.00,
            ),
            Dish(
                title="Лосось в соусе",
                description="Трюфельный соус, лосось, гуакамоле",
                price=1350.00,
            ),
        ]
        dishes_2_1 = [
            Dish(
                title="Johnny Walker Blue Label",
                description="Шотландское виски",
                price=800.00,
            ),
            Dish(title="CAMPO AZUL", description="Мексиканская Текила", price=650.00),
            Dish(
                title="Buzz Light", description="Лучшее американское пиво", price=200.00
            ),
        ]
        dishes_2_2 = [
            Dish(
                title="Prosecco Brut",
                description="Итальянское игристое вино",
                price=1000.00,
            ),
            Dish(
                title="Ned Sauvignon",
                description="Белое вино из Новой Зеландии",
                price=950.00,
            ),
            Dish(
                title="Vihno Verde Rose ",
                description="Португальское красное вино",
                price=800.00,
            ),
        ]
        submenus_1[0].dishes.extend(dishes_1_1)
        submenus_1[1].dishes.extend(dishes_1_2)
        submenus_2[0].dishes.extend(dishes_2_1)
        submenus_2[1].dishes.extend(dishes_2_2)

        menus[0].submenus.extend(submenus_1)
        menus[1].submenus.extend(submenus_2)
        db.session.add_all(menus)
