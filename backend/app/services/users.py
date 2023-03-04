from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app import models, schemas
from app.internal import get_password_hash, verify_password
from fastapi import Depends
from app import dependencies

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(
    username: str, password: str, db: Session = Depends(dependencies.get_db)
):
    user = get_user_email(email=username, db=db)
    print(user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
