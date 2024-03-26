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
    pass
    # """
    # Get all users in a provider.
    #
    # Args:
    #     db (Session): The database session.
    #     provider_id (int): The provider id.
    # """
    # return db.query(models.User).filter(models.User.provider_id == provider_id).all()
