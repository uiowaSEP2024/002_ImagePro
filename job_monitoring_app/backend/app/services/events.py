from .. import models, schemas
from sqlalchemy.orm import Session

from .job_configuration import get_step_configuration_by_composite_key
from .jobs import get_job_by_provider_job_id


def create_event(db: Session, event: schemas.EventCreatePublic, provider):
    job = get_job_by_provider_job_id(db, event.provider_job_id, provider.id)

    params = dict(
        kind=event.kind,
        name=event.name,
        job_id=job.id,
        event_metadata=event.event_metadata,
    )

    if event.tag:
        step_configuration = get_step_configuration_by_composite_key(
            db, job.job_configuration_id, event.tag
        )
        params.update(dict(step_configuration_id=step_configuration.id))

    db_event = models.Event(**params)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def update_event(db: Session, event: schemas.EventUpdate):
    db_update_event = get_event_by_id(db, event.id)

    db_update_event.kind = event.kind
    db_update_event.metadata = event.event_metadata
    db.commit()
    db.refresh(db_update_event)
    return db_update_event
