from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas, services
from app.dependencies import get_db, get_user_from_api_key

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
