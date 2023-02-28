from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .users import User


def test_users():
    db = SessionLocal()
    db_user = User(email="user.email", hashed_password="fake_hashed_password")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
