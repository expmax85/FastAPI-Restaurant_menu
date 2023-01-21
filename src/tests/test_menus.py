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

    def test_create_menu(self, test_app):
        response = test_app.post(
            "api/v1/menus",
            json={"title": "Test menu 1", "description": "Test menu descr 1"},
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["title"] == "Test menu 1"
        assert "id" in data

    @pytest.fixture(scope='class')
    def menu_id(self):
        db_ = TestingSessionLocal()
        menu = actions.menu_orm.get_all(db_)[-1]
        db_.close()
        return menu.id

    def test_get_menu(self, test_app, menu_id):
        response = test_app.get(f"/api/v1/menus/{menu_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "Test menu 1"
        assert data["id"] == str(menu_id)

    def test_get_menus(self, test_app):
        response = test_app.get(f"/api/v1/menus")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1

    def test_update_menu(self, test_app, menu_id):
        response = test_app.patch(f"/api/v1/menus/{menu_id}",
                                json={"title": "Updated menu 1", "description": "Updated menu descr 1"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "Updated menu 1"
        assert data["id"] == str(menu_id)

    def test_delete_menu(self, test_app, menu_id):
        response = test_app.delete(f"/api/v1/menus/{menu_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["status"] is True
        assert data["message"] == 'The menu has been deleted'
