import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import config as settings
from src.database import actions

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestCase:

    @pytest.fixture(scope='class')
    def menu(self, test_app):
        db_ = TestingSessionLocal()
        menu = actions.menu_orm.create(db_, {'title': 'Test menu 1', 'description': 'Test description 1'})
        db_.close()
        return menu.id

    @pytest.fixture(scope='class')
    def submenu(self, test_app, menu):
        db_ = TestingSessionLocal()
        submenu = actions.submenu_orm.create(db_, {'title': 'Test submenu 1', 'description': 'Test subdescription 1'}, menu_id=menu)
        db_.close()
        return submenu.id

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
        db_ = TestingSessionLocal()
        dish = actions.dish_orm.get_all(db_)[-1]
        db_.close()
        return dish.id

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

    def test_clear_db(self, test_app):
        response = test_app.get(
            f"api/v1/menus"
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0
