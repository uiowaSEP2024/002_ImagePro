from app.dependencies import get_db, get_current_user_from_token
from app import schemas, services
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Union


router = APIRouter()
router.tags = ["users"]


@router.post("/users/", response_model=schemas.User)
def create_user(
    user: Union[
        schemas.UserHospitalCreate, schemas.UserProviderCreate, schemas.UserCreate
    ],
    db: Session = Depends(get_db),
):
    if user.role == "hospital":
        return services.create_hospital_user(db=db, user=user)
    elif user.role == "provider":
        return services.create_provider_user(db=db, user=user)
    else:
        return services.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user_from_token),
):
    db_user = services.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/{user_id}/hospital", response_model=schemas.Hospital)
def read_user_hospital(
    user_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user_from_token),
):
    db_user_hospital = services.get_user_hospital(db, user_id=user_id)
    if db_user_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return db_user_hospital


@router.get("/users/{user_id}/provider", response_model=schemas.Provider)
def read_user_provider(
    user_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user_from_token),
):
    db_user_provider = services.get_user_provider(db, user_id=user_id)
    if db_user_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_user_provider
