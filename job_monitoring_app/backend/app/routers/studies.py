from typing import List

from app import schemas, services
from app.dependencies import get_db, get_user_from_api_key, get_current_user_from_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()
router.tags = ["studies"]


@router.post("/studies", response_model=schemas.Study)
def create_study(
    study: schemas.StudyCreate,
    db: Session = Depends(get_db),
    user_provider=Depends(get_user_from_api_key),
):
    provider = services.get_provider_by_user_id(db, user_id=user_provider.id)
    return services.create_study(db=db, study=study, provider=provider)


@router.get("/studies", response_model=List[schemas.Study])
def get_studies(
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    if user.role == schemas.UserRoleEnum.admin:
        return services.get_all_studies(db=db)
    elif user.role == schemas.UserRoleEnum.provider:
        return services.get_studies_for_provider(db=db, user_id=user.id)
    else:
        return services.get_studies_for_hospital(db=db, user_id=user.id)


@router.get("/studies/{study_id}", response_model=schemas.Study)
def get_study(
    study_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    study = services.get_study_by_id(db, study_id=study_id)

    if study is None:
        raise HTTPException(status_code=404, detail="Study not found")

    if user.role == schemas.UserRoleEnum.provider:
        provider = services.get_provider_by_user_id(db, user_id=user.id)
        if provider.id != study.provider_id:
            raise HTTPException(status_code=403, detail="Not allowed")

    if user.role == schemas.UserRoleEnum.hospital:
        hospital = services.get_hospital_by_user_id(db, user_id=user.id)
        if hospital.id != study.hospital_id:
            raise HTTPException(status_code=403, detail="Not allowed")

    return study


@router.get("/studies/{study_id}/events", response_model=List[schemas.Event])
def get_study_events(
    study_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_from_token),
):
    study = services.get_study_by_id(db, study_id=study_id)

    if study is None:
        raise HTTPException(status_code=404, detail="Study not found")

    if user.role == schemas.UserRoleEnum.provider:
        provider = services.get_provider_by_user_id(db, user_id=user.id)
        if provider.id != study.provider_id:
            raise HTTPException(status_code=403, detail="Not allowed")

    if user.role == schemas.UserRoleEnum.hospital:
        hospital = services.get_hospital_by_user_id(db, user_id=user.id)
        if hospital.id != study.hospital_id:
            raise HTTPException(status_code=403, detail="Not allowed")

    return study.events
