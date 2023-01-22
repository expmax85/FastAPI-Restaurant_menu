import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from starlette.testclient import TestClient

from src import config as settings
from src.database import get_db, actions
from src.main import app
from src.models import schemas


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(settings.TEST_DATABASE_URL)
    yield engine


@pytest.fixture(scope="function")
def session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    transaction.rollback()
    connection.close()


#
@pytest.fixture(scope="function")
def test_app(session):
    app.dependency_overrides[get_db] = lambda: session
    with TestClient(app) as c:
        yield c


@pytest.fixture
def menu(session):
    menu = actions.menu_orm.create(session, {'title': 'Test menu 1', 'description': 'Test description 1'})
    return menu.id


@pytest.fixture
def submenu(session, menu):
    submenu = actions.submenu_orm.create(session, {'title': 'Test submenu 1', 'description': 'Test subdescription 1'},
                                         menu_id=menu)
    return submenu.id


@pytest.fixture
def dish(session, submenu):
    dish = actions.dish_orm.create(session, schemas.DishCreate(title='Test dish 2',
                                                               description='Test dish description 2',
                                                               price=14.0),
                                   submenu_id=submenu)
    return dish.id
