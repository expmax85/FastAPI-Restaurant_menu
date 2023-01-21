
def test_create_dish(test_app, menu, submenu):
    response = test_app.post(
        f"api/v1/menus/{menu}/submenus/{submenu}/dishes",
        json={"title": "Test dish 1", "description": "Test dish descr 1", "price": 14.0},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "Test dish 1"
    assert "id" in data


def test_get_dish(test_app, menu, submenu, dish):
    response = test_app.get(f"/api/v1/menus/{menu}/submenus/{submenu}/dishes/{dish}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == 'Test dish 2'
    assert data["price"] == '14.0'
    assert data["id"] == str(dish)


def test_get_dishes(test_app, menu, submenu, dish):
    response = test_app.get(f"/api/v1/menus/{menu}/submenus/{submenu}/dishes")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1


def test_update_dish(test_app, menu, submenu, dish):
    response = test_app.patch(f"/api/v1/menus/{menu}/submenus/{submenu}/dishes/{dish}",
                              json={"title": "Updated dish 1", "price": 16.0})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Updated dish 1"
    assert data["description"] == "Test dish description 2"
    assert data["price"] == "16.0"
    assert data["id"] == str(dish)


def test_delete_dish(test_app, menu, submenu, dish):
    response = test_app.delete(
        f"api/v1/menus/{menu}/submenus/{submenu}/dishes/{dish}"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] is True
    assert data["message"] == 'The dish has been deleted'
