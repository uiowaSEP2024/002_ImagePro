from app import models, schemas
from sqlalchemy.orm import Session
from .users import get_user


def create_job(db: Session, job: schemas.JobCreate, provider):
    db_job = models.Job(
        provider_id=provider.id,
        provider_job_id=job.provider_job_id,
        provider_job_name=job.provider_job_name,
        customer_id=job.customer_id,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_job_by_provider_job_id(db: Session, provider_job_id: str, provider_id: int):
    return (
        db.query(models.Job)
        .filter(
            models.Job.provider_job_id == provider_job_id,
            models.Job.provider_id == provider_id,
        )
        .first()
    )


def get_jobs_for_customer(db: Session, user_id: int):
    return get_user(db, user_id).jobs


def get_jobs_for_provider(db: Session, user_id: int):
    return get_user(db, user_id).provider_jobs


def get_job_by_id(db: Session, job_id: int):
    return db.query(models.Job).get(job_id)
