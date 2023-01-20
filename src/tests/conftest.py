import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from starlette.testclient import TestClient

from src.config import settings
from src.database import get_db
from src.main import app


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    return client
