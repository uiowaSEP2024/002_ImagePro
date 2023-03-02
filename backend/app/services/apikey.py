from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import models, schemas
from app.internal import generate_apikey

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_apikeys(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_apikey_for_user(db: Session, user_id: int):
    db_apikey = models.Apikey(
        key=generate_apikey(),
        user_id=user_id
    )

    db.add(db_apikey)
    db.commit()
    db.refresh(db_apikey)
    return db_apikey
