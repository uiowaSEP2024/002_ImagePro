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
study_configuration_counter = 0


def get_next_user_count():
    global user_counter
    user_counter = user_counter + 1
    return user_counter


def get_next_study_configuration_count():
    global study_configuration_counter
    study_configuration_counter = study_configuration_counter + 1
    return study_configuration_counter


@pytest.fixture(scope="session", autouse=True)
def run_around_tests():
    truncate_all_tables()
    yield


@pytest.fixture
def app_client():
    return TestClient(app)


@pytest.fixture
def db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def random_test_user_no_role(db):
    random_tag = get_next_user_count()
    test_user_no_role = services.create_user(
        db,
        schemas.UserCreate(
            email=f"testuser_{random_tag}@example.com",
            password="abc",
            first_name="random",
            last_name="last",
        ),
    )
    return test_user_no_role


@pytest.fixture
def random_provider_user_with_api_key(db, random_provider_user):
    services.create_apikey_for_user(
        db, random_provider_user.id, key=schemas.ApikeyCreate(note="key")
    )
    db.refresh(random_provider_user)
    return random_provider_user


@pytest.fixture
def study_for_random_user_with_api_key(
    db, random_provider_user_with_api_key, random_study_configuration_factory
):
    study_configuration = random_study_configuration_factory.get()

    study = services.create_study(
        db,
        schemas.StudyCreate(
            provider_study_id="145254",
            hospital_id=random_provider_user_with_api_key.id,
            tag=study_configuration.tag,
        ),
        provider=random_provider_user_with_api_key,
    )
    return study


@pytest.fixture
def random_provider_user(db):
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


@pytest.fixture
def random_hospital_user(db):
    random_tag = get_next_user_count()
    test_hospital_user = services.create_user(
        db,
        schemas.UserCreate(
            email=f"test-hospital-user_{random_tag}@example.com",
            password="abc",
            first_name="first",
            last_name="last",
            role=UserRoleEnum.hospital,
        ),
    )
    return test_hospital_user


@pytest.fixture
def random_admin_user(db):
    random_tag = get_next_user_count()
    test_admin_user = services.create_user(
        db,
        schemas.UserCreate(
            email=f"test-admin-user_{random_tag}@example.com",
            password="abc",
            first_name="first",
            last_name="last",
            role=UserRoleEnum.admin,
        ),
    )
    return test_admin_user


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
def random_test_user_no_role_factory(db):
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
def random_study_configuration_factory(db, random_provider_user):
    class Factory(object):
        @staticmethod
        def get(num_steps=0):
            count = get_next_study_configuration_count()
            test_study_configuration = models.StudyConfiguration(
                tag=f"test_study_{count}",
                name="Test Study",
                provider_id=random_provider_user.id,
                version="0.0." + str(get_next_user_count()),
            )

            for i in range(num_steps):
                test_study_configuration.step_configurations.append(
                    models.StepConfiguration(
                        name=f"Step {i}",
                        tag=f"step_{i}",
                        points=10,
                        study_configuration=test_study_configuration,
                    )
                )

            db.add(test_study_configuration)
            db.commit()
            db.refresh(test_study_configuration)
            return test_study_configuration

    return Factory()
