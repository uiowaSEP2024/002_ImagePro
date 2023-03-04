from tasks import setup_app_settings

setup_app_settings("test")

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
