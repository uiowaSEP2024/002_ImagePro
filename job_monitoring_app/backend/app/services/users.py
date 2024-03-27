from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app import models, schemas
from app.internal import get_password_hash, verify_password

from app.models.hospital_users import hospital_user_association
from app.models.provider_users import provider_user_association

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


def create_hospital_user(db: Session, user: schemas.UserHospitalCreate) -> models.User:
    """
    Creates a new user in the database associated with a hospital.

    Args:
        db (Session): The database session.
        user (schemas.UserHospitalCreate): The user to create.
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
    db.execute(
        hospital_user_association.insert().values(
            user_id=db_user.id, hospital_id=user.hospital_id
        )
    )
    db.commit()
    db.refresh(db_user)
    return db_user


def create_provider_user(db: Session, user: schemas.UserProviderCreate) -> models.User:
    """
    Creates a new user in the database associated with a provider.

    Args:
        db (Session): The database session.
        user (schemas.UserProviderCreate): The user to create.
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
    db.execute(
        provider_user_association.insert().values(
            user_id=db_user.id, provider_id=user.provider_id
        )
    )
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Creates a new admin user in the database.

    Args:
        db (Session): The database session.
        user (schemas.UserHospitalCreate): The user to create.
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


def get_user_hospital(db: Session, user_id: int) -> models.Hospital:
    """
    Retrieves the hospital associated with a user, only for 'hospital' users

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve the hospital for.
    """
    return (
        db.query(models.Hospital)
        .join(hospital_user_association)
        .filter(hospital_user_association.c.user_id == user_id)
        .first()
    )


def get_user_provider(db: Session, user_id: int) -> models.Provider:

    """
    Retrieves the provider associated with a user, only for 'provider' users

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve the provider for.
    """
    return (
        db.query(models.Provider)
        .join(provider_user_association)
        .filter(provider_user_association.c.user_id == user_id)
        .first()
    )
