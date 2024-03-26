import pytest
import sqlalchemy

from config import config
from app.schemas import UserCreate
from app.schemas import UserHospitalCreate
from app.services.users import create_user
from app.services.users import create_hospital_user
from app.schemas.user import UserRoleEnum
from app.schemas.hospital import HospitalCreate
from app.services.hospitals import create_hospital
from app.services.users import get_user_hospital


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


def test_users_hospital_association():
    db = config.db.SessionLocal()

    db_hospital = create_hospital(
        db,
        HospitalCreate.parse_obj(
            {
                "hospital_name": "test_hospital_bobby",
            }
        ),
    )

    db = config.db.SessionLocal()
    db_user = create_hospital_user(
        db,
        UserHospitalCreate.parse_obj(
            {
                "email": "zzz@example.com",
                "password": "abc",
                "first_name": "Bobby",
                "last_name": "Busche",
                "role": UserRoleEnum.hospital,
                "hospital_id": db_hospital.id,
            }
        ),
    )

    assert db_user.email == "zzz@example.com"
    assert db_user.hashed_password is not None
    assert db_user.first_name == "Bobby"
    assert db_user.last_name == "Busche"
    assert db_user.role == UserRoleEnum.hospital
    assert db_user.created_at is not None
    assert get_user_hospital(db, db_user.id).hospital_name == db_hospital.hospital_name
