import json
from typing import Union

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette import status

from app import models, schemas
from app.schemas.pydantic_version import PydanticVersion

from deepdiff import DeepDiff


def get_job_configuration_by_tag(db: Session, tag: str):
    return (
        db.query(models.JobConfiguration)
        .order_by(desc(models.JobConfiguration.created_at))
        .filter(models.JobConfiguration.tag == tag)
        .first()
    )


def create_job_configuration(
    db: Session, provider_id: str, job_configuration: schemas.JobConfigurationCreate
):
    old_configuration = get_job_configuration_by_composite_key(
        db,
        provider_id=provider_id,
        tag=job_configuration.tag,
        version=job_configuration.version,
    )

    if old_configuration is None:
        # Proceed to create the job_configuration if it does not exist yet
        db_job_configuration = models.JobConfiguration(
            provider_id=provider_id,
            tag=job_configuration.tag,
            version=str(job_configuration.version),
            name=job_configuration.name,
        )

        # Create nested step_configurations for the job
        for step_configuration in job_configuration.step_configurations:
            db_job_configuration.step_configurations.append(
                models.StepConfiguration(
                    name=step_configuration.name,
                    tag=step_configuration.tag,
                    points=step_configuration.points,
                )
            )

        db.add(db_job_configuration)
        db.commit()
        db.refresh(db_job_configuration)

        return db_job_configuration

    # Already existing job configuration so check for differences between incoming configuration data and
    # old configuration data
    configuration_data = schemas.JobConfigurationCreate.parse_raw(
        json.dumps(job_configuration.dict(), default=str), content_type="json"
    )

    old_configuration_data = schemas.JobConfigurationCreate.parse_obj(
        {
            **old_configuration.__dict__,
            "step_configurations": [
                s.__dict__ for s in old_configuration.step_configurations
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
                "msg": "You are attempting to create a job configuration with an already existing version, "
                "please update your version and try again",
                "changes": str(differences),
            },
        )

    return old_configuration


def get_job_configuration_by_composite_key(
    db: Session, provider_id: str, tag: str, version: Union[str, PydanticVersion]
):
    """
    Returns a unique job configuration give the composite key comprising the provider_id, tag, and version
    There should be only one job_configuration given these fields.
    """
    return (
        db.query(models.JobConfiguration)
        .filter(
            models.JobConfiguration.tag == tag,
            models.JobConfiguration.provider_id == provider_id,
            models.JobConfiguration.version == str(version),
        )
        .first()
    )
