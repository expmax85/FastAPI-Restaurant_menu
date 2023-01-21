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

    def test_create_submenu(self, test_app, menu):
        response = test_app.post(
            f"api/v1/menus/{menu}/submenus",
            json={"title": "Test submenu 1", "description": "Test submenu descr 1"},
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["title"] == "Test submenu 1"
        assert "id" in data

    @pytest.fixture(scope="class")
    def submenu(self):
        db_ = TestingSessionLocal()
        submenu = actions.submenu_orm.get_all(db_)[-1]
        db_.close()
        return submenu.id

    def test_get_submenu(self, test_app, menu, submenu):
        response = test_app.get(f"/api/v1/menus/{menu}/submenus/{submenu}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "Test submenu 1"
        assert data["id"] == str(submenu)

    def test_get_menus(self, test_app, menu):
        response = test_app.get(f"/api/v1/menus/{menu}/submenus")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1

    def test_update_menu(self, test_app, menu, submenu):
        response = test_app.patch(f"/api/v1/menus/{menu}/submenus/{submenu}",
                                  json={"title": "Updated submenu 1", "description": "Updated submenu descr 1"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "Updated submenu 1"
        assert data["id"] == str(submenu)

    def test_delete_submenu(self, test_app, menu, submenu):
        response = test_app.delete(
            f"api/v1/menus/{menu}/submenus/{submenu}"
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["status"] is True
        assert data["message"] == 'The submenu has been deleted'

    def test_remove_menu(self, test_app, menu):
        test_app.delete(f"api/v1/menus/{menu}")
