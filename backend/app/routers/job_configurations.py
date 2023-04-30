from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas, services
from app.dependencies import get_db, get_user_from_api_key
from app import schemas, services
from app.dependencies import get_db, get_current_user_from_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
def get_job_configuration(
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
