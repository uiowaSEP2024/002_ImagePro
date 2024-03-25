import pytest
import sqlalchemy

from config import config
from app.schemas import UserCreate
from app.services.users import create_user
from app.schemas.user import UserRoleEnum


def test_users_no_role():
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


def test_users_provider_role():
    db = config.db.SessionLocal()
    db_user = create_user(
        db,
        UserCreate.parse_obj(
            {
                "email": "ap@example.com",
                "password": "abc",
                "first_name": "Bob",
                "last_name": "Brown",
                "role": UserRoleEnum.provider,
            }
        ),
    )

    assert db_user.email == "ap@example.com"
    assert db_user.hashed_password is not None
    assert db_user.first_name == "Bob"
    assert db_user.last_name == "Brown"
    assert db_user.role == UserRoleEnum.provider
    assert db_user.created_at is not None


def test_users_hospital_role():
    db = config.db.SessionLocal()
    db_user = create_user(
        db,
        UserCreate.parse_obj(
            {
                "email": "xy@example.com",
                "password": "abc",
                "first_name": "Billy",
                "last_name": "Brown",
                "role": UserRoleEnum.hospital,
            }
        ),
    )

    assert db_user.email == "xy@example.com"
    assert db_user.hashed_password is not None
    assert db_user.first_name == "Billy"
    assert db_user.last_name == "Brown"
    assert db_user.role == UserRoleEnum.hospital
    assert db_user.created_at is not None


def test_users_admin_role():
    db = config.db.SessionLocal()
    db_user = create_user(
        db,
        UserCreate.parse_obj(
            {
                "email": "io@example.com",
                "password": "abc",
                "first_name": "Bobina",
                "last_name": "Brown",
                "role": UserRoleEnum.admin,
            }
        ),
    )

    assert db_user.email == "io@example.com"
    assert db_user.hashed_password is not None
    assert db_user.first_name == "Bobina"
    assert db_user.last_name == "Brown"
    assert db_user.role == UserRoleEnum.admin
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


def test_hospital_user():
    db = config.db.SessionLocal()

    # db_hospital = create_hospital(
    #     db,
    #     HospitalCreate.parse_obj(
    #         {
    #             "hospital_name": "Hospital 1",
    #         }
    #     ),
    # )

    db_user = create_user(
        db,
        UserCreate.parse_obj(
            {
                "email": "jimbrown@example.com",
                "password": "abc",
                "first_name": "Jim",
                "last_name": "Brown",
                "role": UserRoleEnum.hospital,
            }
        ),
    )

    assert db_user.email == "jimbrown@example.com"
    assert db_user.hashed_password is not None
    assert db_user.first_name == "Jim"
    assert db_user.last_name == "Brown"
    assert db_user.created_at is not None
