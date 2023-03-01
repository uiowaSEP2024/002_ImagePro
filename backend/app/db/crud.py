from sqlalchemy.orm import Session

from .models import users


def get_user(db: Session, user_id: int):
    return db.query(users.User).filter(users.User.id == user_id).first()


def create_user(db: Session): # user: schemas.UserCreate)
    # fake_hashed_password = user.password + "notreallyhashed"
    db_user = users.User(email="user.email", hashed_password="fake_hashed_password")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
