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
@router.get("/jobs", response_model=List[schemas.Job])
def get_customer_jobs(
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    if user.role == "customer":
        return services.get_jobs_for_customer(db=db, user_id=user.id)

    return services.get_jobs_for_provider(db=db, user_id=user.id)


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

    if not (user.id in [job.customer_id, job.provider_id]):
        # TODO: add job.provider_id to the list of allowed users that can
        #  access this once we have api key based access? See above comment
        raise HTTPException(status_code=403, detail="Not allowed")

    return job


@router.get("/jobs/{job_id}/events", response_model=List[schemas.Event])
def get_job_events(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    # TODO: see comments from /jobs/{job_id}
    job = services.get_job_by_id(db, job_id=job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if not (user.id in [job.customer_id, job.provider_id]):
        raise HTTPException(status_code=403, detail="Not allowed")

    return job.events
