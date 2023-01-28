import pytest

from src.database import actions


@pytest.mark.asyncio
async def test_create_dish(test_app):
    menu = await actions.menu_orm.create({'title': 'Test menu 1', 'description': 'Test description 1'})
    submenu = await actions.submenu_orm.create({'title': 'Test submenu 1', 'description': 'Test subdescription 1'},
                                               menu_id=menu.id)
    response = await test_app.post(
        f"api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/",
        json={"title": "Test dish 1", "description": "Test dish descr 1", "price": 14.0},
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "Test dish 1"
    assert "id" in data
    await actions.menu_orm.remove(menu.id)


@pytest.mark.asyncio
async def test_get_dish(test_app):
    menu = await actions.menu_orm.create({'title': 'Test menu 1', 'description': 'Test description 1'})
    submenu = await actions.submenu_orm.create({'title': 'Test submenu 1', 'description': 'Test subdescription 1'},
                                               menu_id=menu.id)
    dish = await actions.dish_orm.create({"title": 'Test dish 2', "description": 'Test dish description 2',
                                          "price": 14.0}, submenu_id=submenu.id)
    response = await test_app.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}")

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == dish.title
    assert data["price"] == str(dish.price)
    assert data["id"] == str(dish.id)
    await actions.menu_orm.remove(menu.id)


@pytest.mark.asyncio
async def test_get_dishes(test_app):
    menu = await actions.menu_orm.create({'title': 'Test menu 1', 'description': 'Test description 1'})
    submenu = await actions.submenu_orm.create({'title': 'Test submenu 1', 'description': 'Test subdescription 1'},
                                               menu_id=menu.id)
    await actions.dish_orm.create({"title": 'Test dish 2', "description": 'Test dish description 2',
                                   "price": 14.0}, submenu_id=submenu.id)
    response = await test_app.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/")

    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    await actions.menu_orm.remove(menu.id)


@pytest.mark.asyncio
async def test_update_dish(test_app):
    menu = await actions.menu_orm.create({'title': 'Test menu 1', 'description': 'Test description 1'})
    submenu = await actions.submenu_orm.create({'title': 'Test submenu 1', 'description': 'Test subdescription 1'},
                                               menu_id=menu.id)
    dish = await actions.dish_orm.create({"title": 'Test dish 2', "description": 'Test dish description 2',
                                          "price": 14.0}, submenu_id=submenu.id)
    response = await test_app.patch(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}",
                                    json={"title": "Updated dish 1", "price": 16.0})

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] != dish.title
    assert data["description"] == dish.description
    assert data["price"] != str(dish.price)
    assert data["title"] == "Updated dish 1"
    assert data["price"] == "16.0"
    assert data["id"] == str(dish.id)
    await actions.menu_orm.remove(menu.id)


@pytest.mark.asyncio
async def test_delete_dish(test_app):
    menu = await actions.menu_orm.create({'title': 'Test menu 1', 'description': 'Test description 1'})
    submenu = await actions.submenu_orm.create({'title': 'Test submenu 1', 'description': 'Test subdescription 1'},
                                               menu_id=menu.id)
    dish = await actions.dish_orm.create({"title": 'Test dish 2', "description": 'Test dish description 2',
                                          "price": 14.0}, submenu_id=submenu.id)
    response = await test_app.delete(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}")

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] is True
    assert data["message"] == 'The dish has been deleted'
    dishes = await actions.dish_orm.get_all()
    assert len(dishes) == 0
    await actions.menu_orm.remove(menu.id)
