from app import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import cast
from .jobs import get_job_by_provider_job_id



def create_event(db: Session, event: schemas.EventCreatePublic, provider):
    job = get_job_by_provider_job_id(db, event.provider_job_id, provider.id)
    # print(type(event.metadata))
    db_event = models.Event(kind=event.kind, name=event.name, job_id=job.id, event_metadata=event.metadata)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
