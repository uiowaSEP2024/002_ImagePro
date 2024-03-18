import json
from typing import Union

from app import models, schemas
from app.schemas.pydantic_version import PydanticVersion
from deepdiff import DeepDiff
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette import status


def get_step_configuration_by_composite_key(
    db: Session, study_configuration_id: str, tag: str
) -> models.StepConfiguration:
    """
    Returns a unique step configuration given the composite key comprising the study_configuration_id and tag
    There should be only one step_configuration with a given tag for a given study_configuration_id

    Args:
        db (Session): SQLAlchemy session
        study_configuration_id (str): Study configuration id
        tag (str): Tag
    Returns:
        models.StepConfiguration: Step configuration associated with the given study_configuration_id and tag
    """
    return (
        db.query(models.StepConfiguration)
        .filter(models.StepConfiguration.tag == tag)
        .filter(
            models.StepConfiguration.study_configuration_id == study_configuration_id
        )
        .first()
    )


def get_study_configuration_by_tag(
    db: Session, tag: str, provider_id: int
) -> models.StudyConfiguration:
    """
    Returns a unique study configuration given the tag and provider_id

    Args:
        db (Session): SQLAlchemy session
        tag (str): Tag
        provider_id (int): Provider id
    Returns:
        models.StudyConfiguration: Study configuration associated with the given tag and provider_id
    """
    return (
        db.query(models.StudyConfiguration)
        .order_by(desc(models.StudyConfiguration.created_at))
        .filter(
            models.StudyConfiguration.tag == tag,
            models.StudyConfiguration.provider_id == provider_id,
        )
        .first()
    )


def get_study_configurations_by_tag(
    db: Session, tag: str, provider_id: int
) -> list[models.StudyConfiguration]:
    """
    Returns a list of study configurations given the tag and provider_id
    get's all study configurations for a particular tag

    Args:
        db (Session): SQLAlchemy session
        tag (str): Tag
        provider_id (int): Provider id
    Returns:
        list[models.StudyConfiguration]: List of study configurations associated with the given tag and provider_id
    """
    return (
        db.query(models.StudyConfiguration)
        .order_by(desc(models.StudyConfiguration.created_at))
        .filter(
            models.StudyConfiguration.tag == tag,
            models.StudyConfiguration.provider_id == provider_id,
        )
        .all()
    )


def get_list_of_latest_versions_for_all_study_configurations(
    db: Session, provider_id: int
) -> list[models.StudyConfiguration]:
    """
    Returns a list of the latest study configurations for all tags

    Args:
        db (Session): SQLAlchemy session
        provider_id (int): Provider id
    Returns:
        list[models.StudyConfiguration]: List of latest study configurations for all tags
    """
    return (
        db.query(models.StudyConfiguration)
        .filter(models.StudyConfiguration.provider_id == provider_id)
        .order_by(
            models.StudyConfiguration.tag.desc(),
            models.StudyConfiguration.created_at.desc(),
        )
        .distinct(
            models.StudyConfiguration.tag,
        )
        .all()
    )


def create_study_configuration(
    db: Session, provider_id: str, study_configuration: schemas.StudyConfigurationCreate
) -> models.StudyConfiguration:
    """
    Create a study configuration

    Args:
        db (Session): SQLAlchemy session
        provider_id (str): Provider id
        study_configuration (schemas.StudyConfigurationCreate): Study configuration to create
    Returns:
        models.StudyConfiguration: Created study configuration
    """
    old_configuration = get_study_configuration_by_composite_key(
        db,
        provider_id=provider_id,
        tag=study_configuration.tag,
        version=study_configuration.version,
    )

    if old_configuration is None:
        # Proceed to create the study_configuration if it does not exist yet
        db_study_configuration = models.StudyConfiguration(
            provider_id=provider_id,
            tag=study_configuration.tag,
            version=str(study_configuration.version),
            name=study_configuration.name,
        )

        # Create nested step_configurations for the study
        for step_configuration in study_configuration.step_configurations:
            db_step_configuration = models.StepConfiguration(
                name=step_configuration.name,
                tag=step_configuration.tag,
                points=step_configuration.points,
            )

            step_configuration: schemas.StepConfigurationCreate = step_configuration

            if step_configuration.metadata_configurations is not None:
                for (
                    metadata_configuration
                ) in step_configuration.metadata_configurations:
                    db_step_configuration.metadata_configurations.append(
                        models.MetadataConfiguration(
                            name=metadata_configuration.name,
                            kind=metadata_configuration.kind,
                            units=metadata_configuration.units,
                        )
                    )

            db_study_configuration.step_configurations.append(db_step_configuration)

        db.add(db_study_configuration)
        db.commit()
        db.refresh(db_study_configuration)

        return db_study_configuration

    # Already existing study configuration so check for differences between incoming configuration data and
    # old configuration data
    configuration_data = schemas.StudyConfigurationCreate.parse_raw(
        json.dumps(study_configuration.dict(), default=str), content_type="json"
    )

    old_configuration_data = schemas.StudyConfigurationCreate.parse_obj(
        {
            **old_configuration.__dict__,
            "step_configurations": [
                {
                    **s.__dict__,
                    "metadata_configurations": [
                        m.__dict__ for m in s.metadata_configurations
                    ],
                }
                for s in old_configuration.step_configurations
            ],
        }
    )

    differences = DeepDiff(
        old_configuration_data.dict(),
        configuration_data.dict(),
        ignore_order=True,
    )

    has_differences = len(differences.affected_paths) > 0
    if has_differences:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "You are attempting to create a study configuration with an already existing version, "
                "please update your version and try again",
                "changes": str(differences),
            },
        )

    return old_configuration


def get_study_configuration_by_composite_key(
    db: Session, provider_id: str, tag: str, version: Union[str, PydanticVersion]
) -> models.StudyConfiguration:
    """
    Returns a unique study configuration give the composite key comprising the provider_id, tag, and version
    There should be only one study_configuration given these fields.

    Args:
        db (Session): SQLAlchemy session
        provider_id (str): Provider id
        tag (str): Tag
        version (Union[str, PydanticVersion]): Version
    Returns:
        models.StudyConfiguration: Study configuration associated with the given provider_id, tag, and version
    """
    return (
        db.query(models.StudyConfiguration)
        .filter(
            models.StudyConfiguration.tag == tag,
            models.StudyConfiguration.provider_id == provider_id,
            models.StudyConfiguration.version == str(version),
        )
        .first()
    )


def get_study_configuration_by_id(
    db: Session, study_configuration_id: int
) -> models.StudyConfiguration:
    """
    Get study configuration by id from the database

    Args:
        db (Session): SQLAlchemy session
        study_configuration_id (int): Study configuration id (primary key)
    Returns:
        models.StudyConfiguration: Study configuration with Primary Key study_configuration_id
    """
    return db.query(models.StudyConfiguration).get(study_configuration_id)
