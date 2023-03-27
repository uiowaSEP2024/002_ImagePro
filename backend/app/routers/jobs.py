from typing import List

from app import schemas, services
from app.dependencies import get_db, get_user_from_api_key, get_current_user_from_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["jobs"]


@router.post("/jobs", response_model=schemas.Job)
def create_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    provider=Depends(get_user_from_api_key),
):
    return services.create_job(db=db, job=job, provider=provider)


# TODO: another route for get_provider_jobs
@router.get(
    "/jobs",
)
def get_customer_jobs(
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    return services.get_jobs_for_customer(db=db, user_id=user.id)


@router.get("/jobs/{job_id}", response_model=schemas.Job)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
    # TODO: support getting job with api_key OR maybe new route so they can use provider_job_id?
):
    job = services.get_job_by_id(db, job_id=job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if not (user.id in [job.customer_id]):
        # TODO: add job.provider_id to the list of allowed users that can
        #  access this once we have api key based access? See above comment
        raise HTTPException(status_code=403, detail="Not allowed")

    return job
