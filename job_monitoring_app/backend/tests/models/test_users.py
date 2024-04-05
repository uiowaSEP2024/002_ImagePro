import pytest
import sqlalchemy

from app.schemas import UserCreate
from app.schemas import UserHospitalCreate
from app.schemas import ProviderCreate
from app.services.users import create_user
from app.services.users import create_hospital_user
from app.schemas.user import UserRoleEnum
from app.schemas.hospital import HospitalCreate
from app.services.hospitals import create_hospital
from app.services.users import get_user_hospital
from app.services.providers import create_provider
from app.schemas import UserProviderCreate
from app.services.users import create_provider_user
from app.services.users import get_user_provider


def test_users_no_role(db):
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


def test_users_provider_role(db):
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


def test_users_hospital_role(db):
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


def test_users_admin_role(db):
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


def test_unique_user_email(db):
    with pytest.raises(sqlalchemy.exc.IntegrityError):
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


def test_users_hospital_association(db):
    db_hospital = create_hospital(
        db,
        HospitalCreate.parse_obj(
            {
                "hospital_name": "test_hospital_bobby",
            }
        ),
    )

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


def test_users_provider_association(db):
    db_provider = create_provider(
        db,
        ProviderCreate.parse_obj(
            {
                "provider_name": "test_provider_banjo",
            }
        ),
    )

    db_user = create_provider_user(
        db,
        UserProviderCreate.parse_obj(
            {
                "email": "banjo@example.com",
                "password": "abc",
                "first_name": "Banjo",
                "last_name": "Kazooie",
                "role": UserRoleEnum.provider,
                "provider_id": db_provider.id,
            }
        ),
    )

    assert db_user.email == "banjo@example.com"
    assert db_user.hashed_password is not None
    assert db_user.first_name == "Banjo"
    assert db_user.last_name == "Kazooie"
    assert db_user.role == UserRoleEnum.provider
    assert db_user.created_at is not None
    assert get_user_provider(db, db_user.id).provider_name == db_provider.provider_name
