from sqlalchemy.orm import Session
from app import models, schemas


def create_provider(db: Session, provider: schemas.ProviderCreate) -> models.Provider:
    """
    Creates a new provider in the database.

    Args:
        db (Session): The database session.
        provider (schemas.ProviderCreate): The provider to create.
    """

    db_provider = models.Provider(provider_name=provider.provider_name)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


def get_provider_users(db: Session, provider_id: int) -> models.User:
    """
    Get all users in a provider.

    Args:
        db (Session): The database session.
        provider_id (int): The provider id.
    """
    return (
        db.query(models.User)
        .join(models.ProviderUsers)
        .filter(models.ProviderUsers.provider_id == provider_id)
        .all()
    )


def get_all_providers(db: Session) -> models.Provider:
    """
    Get all providers in the database.

    Args:
        db (Session): The database session.
    """
    return db.query(models.Provider).all()


def get_provider_by_id(db: Session, provider_id: int) -> models.Provider:
    """
    Get a provider by id.

    Args:
        db (Session): The database session.
        provider_id (int): The provider id.
    """
    return db.query(models.Provider).get(provider_id)


def get_provider_by_user_id(db: Session, user_id: int) -> models.Provider:
    """
    Get a provider by a user id.

    Args:
        db (Session): The database session.
        user_id (int): The provider id.
    """
    provider_user = (
        db.query(models.ProviderUsers)
        .filter(models.ProviderUsers.user_id == user_id)
        .first()
    )
    print(provider_user)
    if provider_user:
        provider = get_provider_by_id(db, provider_user.provider_id)
        return provider
    return None
