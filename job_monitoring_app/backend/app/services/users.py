from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app import models, schemas
from app.internal import get_password_hash, verify_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int) -> models.User:
    """
    Retrieves a user from the database by ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        models.User: The user retrieved from the database.
    """
    return db.query(models.User).get(user_id)


def get_user_by_email(db: Session, email: str) -> models.User:
    """
    Retrieves a user from the database by email.

    Args:
        db (Session): The database session.
        email (str): The email of the user to retrieve.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Creates a new user in the database.

    Args:
        db (Session): The database session.
        user (schemas.UserCreate): The user to create.
    """
    db_user = models.User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> models.User:
    """
    Authenticates a user by username and password.

    Args:
        db (Session): The database session.
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    """

    user = get_user_by_email(email=username, db=db)
    # print(user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
