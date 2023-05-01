from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, services, models
from app.dependencies import get_db, get_user_from_api_key
from app import schemas, services
from app.dependencies import get_db, get_current_user_from_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Union, List

router = APIRouter()
router.tags = ["job_configurations"]


@router.post("/job_configurations", response_model=schemas.JobConfiguration)
def create_job(
    job_configuration: schemas.JobConfigurationCreate,
    db: Session = Depends(get_db),
    provider=Depends(get_user_from_api_key),
):
    return services.create_job_configuration(
        db, provider_id=provider.id, job_configuration=job_configuration
    )


@router.get(
    "/job_configurations/{job_configuration_id}",
    response_model=schemas.JobConfiguration,
)
def get_job_configuration_by_id(
    job_configuration_id: int,
    db: Session = Depends(get_db),
    provider=Depends(get_current_user_from_token),
):
    job_configuration = services.get_job_configuration_by_id(
        db, job_configuration_id=job_configuration_id
    )

    if job_configuration is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if not (provider.id in [job_configuration.provider_id]):
        raise HTTPException(status_code=403, detail="Not allowed")

    return job_configuration


@router.get("/job_configurations/", response_model=List[schemas.JobConfiguration])
def get_job_configurations_by_tag_and_version(
    tag: Union[str, None] = None,
    version: Union[str, None] = None,
    db: Session = Depends(get_db),
    provider=Depends(get_current_user_from_token),
):
    job_configurations = None

    job_configurations = (
        services.get_list_of_latest_versions_for_all_job_configurations(db, provider.id)
    )

    # case 1: get specific configuration if both tag and version are provided
    if tag and (type(version) is str and version != "latest"):
        job_configurations = [
            services.get_job_configuration_by_composite_key(
                db, provider.id, tag, version
            )
        ]
    # case 2: get the latest job configuration for a specific tag
    elif tag and version == "latest":
        job_configurations = [
            services.get_job_configuration_by_tag(db, tag, provider.id)
        ]
    # case 3: get all job configurations for a particular tag
    elif tag and version is None:
        job_configurations = [
            job_configuration
            for job_configuration in services.get_job_configurations_by_tag(
                db, tag, provider.id
            )
        ]
    # case 4: get latest version for all
    elif tag is None and (version is None or version == "latest"):
        job_configurations = (
            services.get_list_of_latest_versions_for_all_job_configurations(
                db, provider.id
            )
        )
    if job_configurations is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": f"Could not find job configuration(s) for tag: {tag} and version: {version}"
            },
        )

    return job_configurations
