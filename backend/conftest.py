import pytest
from app.main import app
from app.models.base import truncate_all_tables
from fastapi.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def run_around_tests():
    truncate_all_tables()
    yield


@pytest.fixture
def app_client():
    return TestClient(app)
