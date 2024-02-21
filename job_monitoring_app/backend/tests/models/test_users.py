import pytest
import sqlalchemy

from ...config import config
from ...app.schemas.user import UserCreate
from ...app.services.users import create_user


def test_users():
    db = config.db.SessionLocal()
    db_user = create_user(
        db,
        UserCreate.parse_obj(
            {
                "email": "jimbrown@example.com",
                "password": "abc",
                "first_name": "Jim",
                "last_name": "Brown",
            }
        ),
    )

    assert db_user.email == "jimbrown@example.com"
    assert db_user.hashed_password is not None
    assert db_user.first_name == "Jim"
    assert db_user.last_name == "Brown"
    assert db_user.created_at is not None


def test_unique_user_email():
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db = config.db.SessionLocal()
        create_user(
            db,
            UserCreate.parse_obj(
                {
                    "email": "jimbrown@example.com",
                    "password": "abc",
                    "first_name": "Jim",
                    "last_name": "Brown",
                }
            ),
        )

        create_user(
            db,
            UserCreate.parse_obj(
                {
                    "email": "jimbrown@example.com",
                    "password": "abc",
                    "first_name": "Jim",
                    "last_name": "Brown",
                }
            ),
        )
