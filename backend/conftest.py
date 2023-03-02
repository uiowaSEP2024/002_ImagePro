import pytest
from app.db.database import ensure_tables_created, ensure_tables_dropped
from app.main import app

from fastapi.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def run_around_tests():
    ensure_tables_dropped()
    ensure_tables_created()
    yield


@pytest.fixture
def app_client():
    return TestClient(app)

