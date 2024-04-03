from config import config

from app.schemas import ProviderCreate
from app.services.providers import create_provider
from app.schemas import UserProviderCreate
from app.services.users import create_provider_user
from app.schemas.user import UserRoleEnum
from app.services.providers import get_provider_users, get_provider_by_id


def test_provider_creation():
    db = config.db.SessionLocal()
    db_provider = create_provider(
        db,
        ProviderCreate.parse_obj(
            {
                "provider_name": "test_provider",
            }
        ),
    )

    assert db_provider.provider_name == "test_provider"
    assert db_provider.created_at is not None


def test_provider_users():
    db = config.db.SessionLocal()

    db_provider_1 = create_provider(
        db,
        ProviderCreate.parse_obj(
            {
                "provider_name": "test_provider_1",
            }
        ),
    )

    db_provider_2 = create_provider(
        db,
        ProviderCreate.parse_obj(
            {
                "provider_name": "test_provider_2",
            }
        ),
    )

    db_user_1 = create_provider_user(
        db,
        UserProviderCreate.parse_obj(
            {
                "email": "ping_pong@example.com",
                "password": "abc",
                "first_name": "Ping",
                "last_name": "Pong",
                "role": UserRoleEnum.provider,
                "provider_id": db_provider_1.id,
            }
        ),
    )

    db_user_2 = create_provider_user(
        db,
        UserProviderCreate.parse_obj(
            {
                "email": "kbryant@example.com",
                "password": "abc",
                "first_name": "Kobe",
                "last_name": "Bryant",
                "role": UserRoleEnum.provider,
                "provider_id": db_provider_2.id,
            }
        ),
    )

    db_user_3 = create_provider_user(
        db,
        UserProviderCreate.parse_obj(
            {
                "email": "jlemos@example.com",
                "password": "abc",
                "first_name": "John",
                "last_name": "Lemos",
                "role": UserRoleEnum.provider,
                "provider_id": db_provider_1.id,
            }
        ),
    )

    provider_1_users = get_provider_users(db, db_provider_1.id)
    assert len(provider_1_users) == 2
    assert provider_1_users[0].first_name == db_user_1.first_name
    assert provider_1_users[1].first_name == db_user_3.first_name

    provider_2_users = get_provider_users(db, db_provider_2.id)
    assert len(provider_2_users) == 1
    assert provider_2_users[0].first_name == db_user_2.first_name


def test_get_provider_by_id():
    db = config.db.SessionLocal()

    db_provider_1 = create_provider(
        db,
        ProviderCreate.parse_obj(
            {
                "provider_name": "test_provider_1",
            }
        ),
    )

    provider = get_provider_by_id(db, db_provider_1.id)
    assert provider.id == db_provider_1.id
    assert provider.provider_name == db_provider_1.provider_name
