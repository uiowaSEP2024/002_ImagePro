from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import models
from app.internal import generate_apikey
from app.services import get_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_apikeys(db: Session, user_id: int):
    return get_user(db, user_id).apikeys


def create_apikey_for_user(db: Session, user_id: int):
    db_apikey = models.Apikey(key=generate_apikey(), user_id=user_id)

    db.add(db_apikey)
    db.commit()
    db.refresh(db_apikey)
    return db_apikey
