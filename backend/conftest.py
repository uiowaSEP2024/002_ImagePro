import os
import random

import pytest
from app import schemas, services, models
from app.models.base import truncate_all_tables
from fastapi.testclient import TestClient

from app.schemas.user import UserRoleEnum
from config import config

from app.main import app

# NB: this should happen before any app imports to ensure the environment is set

config.setup("test")

user_counter = 0
job_configuration_counter = 0


def get_next_user_count():
    global user_counter
    user_counter = user_counter + 1
    return user_counter


def get_next_job_configuration_count():
    global job_configuration_counter
    job_configuration_counter = job_configuration_counter + 1
    return job_configuration_counter


@pytest.fixture(scope="session", autouse=True)
def run_around_tests():
    truncate_all_tables()
    yield


@pytest.fixture
def app_client():
    return TestClient(app)


@pytest.fixture
def db():
    return config.db.SessionLocal()


@pytest.fixture
def random_test_user(db):
    random_tag = get_next_user_count()
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
    services.create_apikey_for_user(
        db, random_provider_user.id, key=schemas.ApikeyCreate(note="key")
    )
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
    random_tag = get_next_user_count()
    test_provider_user = services.create_user(
        db,
        schemas.UserCreate(
            email=f"test-provider-user_{random_tag}@example.com",
            password="abc",
            first_name="first",
            last_name="last",
            role=UserRoleEnum.provider,
        ),
    )
    return test_provider_user


# Convenience fixture factory for generating multiple
# users for a test. See https://stackoverflow.com/a/21590140
@pytest.fixture
def random_test_user_factory(db):
    class Factory(object):
        @staticmethod
        def get():
            random_tag = get_next_user_count()
            test_user = services.create_user(
                db,
                schemas.UserCreate(
                    email=f"testuser_{random_tag}@example.com",
                    password="abc",
                    first_name="first",
                    last_name="last",
                ),
            )
            return test_user

    return Factory()


@pytest.fixture
def random_job_configuration_factory(db, random_provider_user):
    class Factory(object):
        @staticmethod
        def get(num_steps=0):
            count = get_next_job_configuration_count()
            test_job_configuration = models.JobConfiguration(
                tag=f"test_job_{count}",
                name="Test Job",
                provider_id=random_provider_user.id,
                version="0.0." + str(get_next_user_count()),
            )

            if num_steps > 0:
                [
                    test_job_configuration.step_configurations.append(
                        models.StepConfiguration(
                            name=f"Step {i}",
                            tag=f"step_{i}",
                            points=10,
                            job_configuration=test_job_configuration,
                        )
                    )
                    for i in range(num_steps)
                ]

            db.add(test_job_configuration)
            db.commit()
            db.refresh(test_job_configuration)
            return test_job_configuration

    return Factory()
