from sqlalchemy.orm import Session
from app import models, schemas

from app.models.provider_users import provider_user_association


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
        .join(provider_user_association)
        .filter(provider_user_association.c.provider_id == provider_id)
        .all()
    )
