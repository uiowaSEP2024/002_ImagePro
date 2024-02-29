from typing import List

from app import schemas, services
from app.dependencies import get_db, get_user_from_api_key, get_current_user_from_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["studies"]


@router.post("/studies", response_model=schemas.Study)
def create_study(
    study: schemas.studyCreate,
    db: Session = Depends(get_db),
    provider=Depends(get_user_from_api_key),
):
    return services.create_study(db=db, study=study, provider=provider)


# TODO: another route for get_provider_studies
@router.get("/studies", response_model=List[schemas.Study])
def get_customer_studies(
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    if user.role == "customer":
        return services.get_studies_for_customer(db=db, user_id=user.id)

    return services.get_studies_for_provider(db=db, user_id=user.id)


@router.get("/studies/{study_id}", response_model=schemas.Study)
def get_study(
    study_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
    # TODO: support getting study with api_key OR maybe new route so they can use provider_study_id?
):
    study = services.get_study_by_id(db, study_id=study_id)

    if study is None:
        raise HTTPException(status_code=404, detail="Study not found")

    if user.id not in [study.hospital_id, study.provider_id]:
        # TODO: add study.provider_id to the list of allowed users that can
        #  access this once we have api key based access? See above comment
        raise HTTPException(status_code=403, detail="Not allowed")

    return study


@router.get("/studies/{study_id}/events", response_model=List[schemas.Event])
def get_study_events(
    study_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    # TODO: see comments from /studies/{study_id}
    study = services.get_study_by_id(db, study_id=study_id)

    if study is None:
        raise HTTPException(status_code=404, detail="Study not found")

    if user.id not in [study.hospital_id, study.provider_id]:
        raise HTTPException(status_code=403, detail="Not allowed")

    return study.events
