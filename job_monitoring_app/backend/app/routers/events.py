from app import schemas, services
from app.dependencies import get_db, get_user_from_api_key
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["events"]


@router.post("/events", response_model=schemas.Event)
def create_event(
    event: schemas.EventCreatePublic,
    db: Session = Depends(get_db),
    provider=Depends(get_user_from_api_key),
):
    return services.create_event(db=db, event=event, provider=provider)


@router.post("/events/{event_id}", response_model=schemas.Event)
def update_event(
    event_id: int,
    event: schemas.EventUpdate,
    db: Session = Depends(get_db),
):
    return services.update_event(db=db, event=event)
