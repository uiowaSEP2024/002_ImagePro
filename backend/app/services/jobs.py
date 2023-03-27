from app import models, schemas
from sqlalchemy.orm import Session


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
