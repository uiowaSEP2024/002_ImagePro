import random

from tasks import setup_app_settings

# NB: this should happen before any app imports to ensure the environment is set
setup_app_settings("test")

from app import services, schemas
import pytest
from app.models.base import truncate_all_tables

from fastapi.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def run_around_tests():
    truncate_all_tables()
    yield


@pytest.fixture
def app_client():
    from app.main import app

    return TestClient(app)


@pytest.fixture
def db():
    from config.database import SessionLocal

    return SessionLocal()


@pytest.fixture
def random_test_user(db):
    random_tag = random.randint(0, 10000)
    test_user = services.create_user(
        db,
        schemas.UserCreate(email=f"testuser_{random_tag}@example.com", password="abc"),
    )
    return test_user
