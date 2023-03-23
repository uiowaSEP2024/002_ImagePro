from app import schemas, services
from app.dependencies import get_db, get_user_from_api_key
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["jobs"]


@router.post("/jobs/", response_model=schemas.Job)
def create_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    provider=Depends(get_user_from_api_key),
):
    return services.create_job(db=db, job=job, provider=provider)
