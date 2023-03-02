import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.database import SessionLocal, ensure_tables_created
from app.schemas import UserCreate
from app.db.crud import create_user


def test_users():
    db = SessionLocal()
    db_user = create_user(
        db, UserCreate.parse_obj({"email": "jimbrown@example.com", "password": "abc"})
    )

    assert db_user.email == "jimbrown@example.com"
    assert db_user.hashed_password is not None


def test_unique_user_email():
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db = SessionLocal()
        create_user(
            db,
            UserCreate.parse_obj({"email": "jimbrown@example.com", "password": "abc"}),
        )

        create_user(
            db,
            UserCreate.parse_obj({"email": "jimbrown@example.com", "password": "abc"}),
        )
