from fastapi import HTTPException
from starlette import status

from app import models, schemas
from sqlalchemy.orm import Session

from .study_configuration import get_study_configuration_by_tag
from .providers import get_provider_by_user_id
from .hospitals import get_hospital_by_user_id


def create_study(
    db: Session, study: schemas.StudyCreate, provider: models.Provider
) -> models.Study:
    """
    Create a new study for a provider, add it to the database, and return the study.

    Args:
        db (Session): Database session
        study (schemas.StudyCreate): Study information
        provider (models.Provider): Provider information
    Returns:
        models.Study: The newly created Study
    """
    study_configuration = get_study_configuration_by_tag(db, study.tag, provider.id)

    if study_configuration is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid study configuration tag",
        )

    db_study = models.Study(
        provider_id=provider.id,
        provider_study_id=study.provider_study_id,
        hospital_id=study.hospital_id,
        study_configuration=study_configuration,
    )

    db.add(db_study)
    db.commit()
    db.refresh(db_study)
    return db_study


def get_study_by_provider_study_id(
    db: Session, provider_study_id: str, provider_id: int
) -> models.Study:
    """
    Get a study by its provider_study_id and provider_id

    Args:
        db (Session): Database session
        provider_study_id (str): The provider's study id
        provider_id (int): The provider's user id
    Returns:
        models.Study: The study
    """
    return (
        db.query(models.Study)
        .filter(
            models.Study.provider_study_id == provider_study_id,
            models.Study.provider_id == provider_id,
        )
        .first()
    )


def get_all_studies(db: Session) -> list[models.Study]:
    """
    Get all studies for every user in the database

    Args:
        db (Session): Database session
    Returns:
        list[models.Study]: List of studies
    """
    return db.query(models.Study).all()


def get_studies_for_hospital(db: Session, user_id: int) -> list[models.Study]:
    """
    Get all studies associated with the hospital with the given user_id

    Args:
        db (Session): Database session
        user_id (int): The user id
    Returns:
        list[models.Study]: List of studies
    """
    # get hospital associated with user from join table
    hospital = get_hospital_by_user_id(db, user_id)
    # get all studies associated with that hospital
    return hospital.studies


def get_studies_for_provider(db: Session, user_id: int) -> list[models.Study]:
    """
    Get all studies associated with the provider with the given user_id

    Args:
        db (Session): Database session
        user_id (int): The user id
    Returns:
        list[models.Study]: List of studies
    """
    # get provider associated with user from join table
    provider = get_provider_by_user_id(db, user_id)
    # get all studies associated with that provider
    return provider.studies


def get_study_by_id(db: Session, study_id: int) -> models.Study:
    """
    Get a study by its id

    Args:
        db (Session): Database session
        study_id (int): The study id
    Returns:
        models.Study: The study with the given id
    """
    return db.query(models.Study).get(study_id)
