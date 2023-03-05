from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import models, schemas
from app.internal import get_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).get(user_id)


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
