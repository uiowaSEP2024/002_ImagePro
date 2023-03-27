import random

from tasks import setup_app_settings

# NB: this should happen before any app imports to ensure the environment is set
setup_app_settings("test")

import pytest
from app import schemas, services
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
    random_tag = random.randint(0, 1000000)
    test_user = services.create_user(
        db,
        schemas.UserCreate(
            email=f"testuser_{random_tag}@example.com",
            password="abc",
            first_name="random",
            last_name="last",
        ),
    )
    return test_user


@pytest.fixture
def random_provider_user_with_api_key(db, random_provider_user):
    services.create_apikey_for_user(db, random_provider_user.id)
    db.refresh(random_provider_user)
    return random_provider_user


@pytest.fixture
def job_for_random_user_with_api_key(db, random_provider_user_with_api_key):
    job = services.create_job(
        db,
        schemas.JobCreate(
            provider_job_id="145254",
            customer_id=random_provider_user_with_api_key.id,
            provider_job_name="Scanning",
        ),
        provider=random_provider_user_with_api_key,
    )
    return job


@pytest.fixture
def random_provider_user(db):
    # TODO: update to actually create a 'provider' user
    random_tag = random.randint(0, 10000)
    test_provider_user = services.create_user(
        db,
        schemas.UserCreate(
            email=f"test-provider-user_{random_tag}@example.com",
            password="abc",
            first_name="first",
            last_name="last",
        ),
    )
    return test_provider_user


# Convenience fixture factory for generating multiple
# users for a test. See https://stackoverflow.com/a/21590140
@pytest.fixture
def random_test_user_factory(db):
    class ThingFactory(object):
        @staticmethod
        def get():
            random_tag = random.randint(0, 1000000)
            test_user = services.create_user(
                db,
                schemas.UserCreate(
                    email=f"testuser_{random_tag}@example.com", password="abc", first_name="first", last_name="last"
                ),
            )
            return test_user

    return ThingFactory()
