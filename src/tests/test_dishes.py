import pytest


class TestCase:

    @pytest.fixture(scope='class')
    def menu(self, test_app):
        data = test_app.post(
            f"api/v1/menus",
            json={"title": "Test menu 1", "description": "Test menu descr 1"},
        )
        return int(data.json()['id'])

    @pytest.fixture(scope='class')
    def submenu(self, test_app, menu):
        data = test_app.post(
            f"api/v1/menus/{menu}/submenus",
            json={"title": "Test submenu 1", "description": "Test submenu descr 1"},
        )
        return int(data.json()['id'])

    def test_create_dish(self, test_app, menu, submenu):
        response = test_app.post(
            f"api/v1/menus/{menu}/submenus/{submenu}/dishes",
            json={"title": "Test dish 1", "description": "Test dish descr 1", "price": 14.0},
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["title"] == "Test dish 1"
        assert "id" in data

    @pytest.fixture(scope="class")
    def dish(self):
        return 1

    def test_get_dish(self, test_app, menu, submenu, dish):
        response = test_app.get(f"/api/v1/menus/{menu}/submenus/{submenu}/dishes/{dish}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "Test dish 1"
        assert data["price"] == "14.0"
        assert data["id"] == str(dish)

    def test_get_dishes(self, test_app, menu, submenu):
        response = test_app.get(f"/api/v1/menus/{menu}/submenus/{submenu}/dishes")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1

    def test_update_dish(self, test_app, menu, submenu, dish):
        response = test_app.patch(f"/api/v1/menus/{menu}/submenus/{submenu}/dishes/{dish}",
                                  json={"title": "Updated dish 1", "price": 16.0})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "Updated dish 1"
        assert data["description"] == "Test dish descr 1"
        assert data["price"] == "16.0"
        assert data["id"] == str(dish)

    def test_delete_dish(self, test_app, menu, submenu, dish):
        response = test_app.delete(
            f"api/v1/menus/{menu}/submenus/{submenu}/dishes/{dish}"
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["status"] is True
        assert data["message"] == 'The dish has been deleted'

    def test_remove_menu(self, test_app, menu):
        test_app.delete(f"api/v1/menus/{menu}")
