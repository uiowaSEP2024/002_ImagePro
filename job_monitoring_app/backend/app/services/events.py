from app import models, schemas  # TODO: Fix imports
from sqlalchemy.orm import Session

from .job_configuration import get_step_configuration_by_composite_key
from .studies import get_study_by_provider_study_id


# A provider is a user, but a user is not necessarily a provider. A provider is a user that has a role of "provider"
# users can be providers or hospitals.  It is assumed that providers are the only ones creating events since they are running the studies


def create_event(
    db: Session, event: schemas.EventCreatePublic, provider: models.User
) -> models.Event:
    """
    Create an event for a study


    Args:
        db (Session): SQLAlchemy session
        event (schemas.EventCreatePublic): Event to create
        provider: Provider
    Returns:
        models.Event: Created event
    """
    study: models.study = get_study_by_provider_study_id(
        db, event.provider_study_id, provider.id
    )

    params = dict(
        kind=event.kind,
        name=event.name,
        study_id=study.id,
        event_metadata=event.event_metadata,
    )
    # If the event has a tag, we need to find the step_configuration_id???
    # What is the purpose of the tag??
    if event.tag:
        step_configuration = get_step_configuration_by_composite_key(
            db, study.job_configuration_id, event.tag
        )
        # TODO: Make note of how this is actually working and add it to the documentation
        # This seems like a weird way to do this? Does it just update the dictionary?
        # Why not just add the step_configuration_id to the dictionary in the first place?

        params.update(dict(step_configuration_id=step_configuration.id))

    db_event = models.Event(**params)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event_by_id(db: Session, event_id: int) -> models.Event:
    """
    Get event by id from the database

    Args:
        db (Session): SQLAlchemy session
        event_id (int): Event id (primary key)

    Returns:
        models.Event: Event
    """
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def update_event(db: Session, event: schemas.EventUpdate) -> models.Event:
    """
    Update an event in the database
    This function takes an eventUpdate schema consisting of the event id, new status, and new metadata
    and updates the corresponding event in the database. This is called when an orthanc_data_logging agent
    updates an event that is part of an ongoing study

    Args:
        db (Session): SQLAlchemy session
        event (schemas.EventUpdate): Event to update
    returns:
        models.Event: The Updated event
    """
    db_update_event = get_event_by_id(db, event.id)
    if db_update_event is None:
        raise ValueError("Event not found")

    db_update_event.kind = event.kind
    db_update_event.event_metadata = event.event_metadata
    db.commit()
    db.refresh(db_update_event)
    return db_update_event
